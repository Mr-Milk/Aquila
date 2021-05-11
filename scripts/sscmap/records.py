import os
from ast import literal_eval
from collections import Counter
from pathlib import Path
from typing import List, Optional, Union
from uuid import uuid4
from zipfile import ZipFile

import pandas as pd
import scanpy as sc
import spatialtis as st
import sqlalchemy
import ujson
from anndata import AnnData

from .db import CellExp, CellInfo, DataRecord, DataStats, ROIInfo, init_db
from .guards import Global
from .meta import RecordMeta


class Record:
    # Database Table
    DataRecord: Optional[pd.DataFrame] = None
    DataStats: Optional[pd.DataFrame] = None
    CellInfo: Optional[pd.DataFrame] = None
    ROIInfo: Optional[pd.DataFrame] = None
    CellExp: Optional[pd.DataFrame] = None

    # ROI Table
    roi_meta: Optional[pd.DataFrame] = None
    shannon_entropy_tb: Optional[pd.DataFrame] = None
    altieri_entropy_tb: Optional[pd.DataFrame] = None

    # Analysis Table
    cell_components_tb: Optional[pd.DataFrame] = None
    cell_density_tb: Optional[pd.DataFrame] = None
    co_expression_tb: Optional[pd.DataFrame] = None
    cell_interaction_tb: Optional[pd.DataFrame] = None

    # Misc
    data_id: Optional[str] = None
    computed: Optional[bool] = None
    meta: Optional[RecordMeta] = None

    def __init__(
        self,
        data: AnnData,
        groups_keys: Optional[List[str]] = None,
        cell_type_key: Optional[str] = "cell_type",
        markers_key: Optional[str] = "markers",
        centroid_key: Optional[str] = "centroid",
        cell_x_key: Optional[str] = None,
        cell_y_key: Optional[str] = None,
        force: bool = False,
        engine: Optional[sqlalchemy.engine.Engine] = None,
        export: Union[Path, str, None] = None,
    ):
        self.data = data.copy()
        self.groups_keys = groups_keys
        self.cell_type_key = cell_type_key
        self.markers_key = markers_key
        self.centroid_key = centroid_key
        self.cell_x_key = cell_x_key
        self.cell_y_key = cell_y_key
        self.force = force

        if self.cell_type_key is not None:
            self.data.obs.rename(
                columns={self.cell_type_key: "cell_type"}, inplace=True
            )
            self.cell_type_key = "cell_type"

        if engine is None:
            self.engine = Global.engine

        if export is None:
            self.export = Global.export

        if engine is not None:
            init_db(engine)
            self.engine = engine

        if export is not None:
            if isinstance(export, str):
                export = Path(export)
            self.export = export

    def ok(self, expand=5, export=None, static=False, zipped=True):
        self.run_analysis(expand)
        self.get_db_table()
        self.to_static(export, static, zipped)
        self.to_db()

    def set_meta(self, doi=None, data_id=None, **kwargs):
        self.meta = RecordMeta(**kwargs).set_id(doi=doi, data_id=data_id)
        self.data_id = self.meta.data_id
        if self.cell_type_key is not None:
            self.meta.has_cell_type = True
        return self

    def run_analysis(self, expand=5):
        st.CONFIG.CELL_TYPE_KEY = self.cell_type_key
        st.CONFIG.EXP_OBS = self.groups_keys
        st.CONFIG.CENTROID_KEY = self.centroid_key
        st.CONFIG.MARKER_KEY = self.markers_key
        st.CONFIG.VERBOSE = True

        sc.pp.filter_genes(self.data, min_cells=100)
        # To eliminate the negative value, we need to transform all the data to positive
        # To preserve the distribution, we scale everything to (0, 1)
        if self.meta.molecule.name == "Protein":
            self.data.X = (self.data.X - self.data.X.min()) / (
                self.data.X.max() - self.data.X.min()
            )
        sc.pp.normalize_total(self.data, target_sum=100)
        sc.pp.log1p(self.data)
        sc.pp.highly_variable_genes(self.data, min_mean=0.0125, min_disp=0.5)

        self.meta.cell_count, self.meta.marker_count = self.data.shape
        print(
            f"Data record {self.meta.data_id} has {self.meta.cell_count} cells and "
            f"{self.meta.marker_count} markers."
        )

        selected_markers = []
        for m, hv in zip(
            self.data.var[self.markers_key], self.data.var.highly_variable
        ):
            if hv:
                selected_markers.append(m)

        # iterative find neighbors until NN reach [4.5, 7)
        while True:
            st.find_neighbors(self.data, expand=expand, count=True)
            neighbors_count = self.data.obs.cell_neighbors_count.mean()
            if neighbors_count <= 4.5:
                expand += 2
            elif neighbors_count > 7:
                expand -= 2
            else:
                break
        print(f"Current neighbor count {neighbors_count}")
        self.co_expression_tb = st.spatial_co_expression(
            self.data, selected_markers=selected_markers, corr_cutoff=0.5
        ).result

        if self.meta.has_cell_type:
            self.cell_components_tb = st.cell_components(self.data).result
            if self.meta.resolution == -1:
                ratio = 1
            else:
                ratio = (
                    self.meta.resolution / 10 ** 6
                )  # The resolution is nanometer, convert to mm
            self.cell_density_tb = st.cell_density(self.data, ratio=ratio).result
            self.shannon_entropy_tb = st.spatial_heterogeneity(
                self.data, method="shannon"
            ).result
            self.altieri_entropy_tb = st.spatial_heterogeneity(
                self.data, method="altieri"
            ).result
            self.cell_interaction_tb = st.neighborhood_analysis(
                self.data, order=False
            ).result

            self.shannon_entropy_tb.rename(
                columns={"heterogeneity": "shannon_entropy"}, inplace=True
            )
            self.altieri_entropy_tb.rename(
                columns={"heterogeneity": "altieri_entropy"}, inplace=True
            )

        return self

    def roi_id(self):
        roi_id = []
        for n, df in self.data.obs.groupby(self.groups_keys):
            uid = str(uuid4())
            roi_id += [uid for _ in range(len(df))]

        self.data.obs["roi_id"] = roi_id
        self.roi_meta = self.data.obs[["roi_id"] + self.groups_keys].drop_duplicates()
        if self.meta.has_cell_type:
            self.roi_meta = self.roi_meta.merge(
                self.shannon_entropy_tb.merge(
                    self.altieri_entropy_tb, on=self.groups_keys
                ),
                on=self.groups_keys,
            )
        else:
            self.roi_meta["shannon_entropy"] = 0
            self.roi_meta["altieri_entropy"] = 0

    def cell_x_y(self):
        if (self.cell_x_key is None) | (self.cell_y_key is None):
            cent = self.data.obs[self.centroid_key].tolist()
            elem = cent[0]
            if isinstance(elem, str):
                cent = [literal_eval(c) for c in cent]
            cell_x, cell_y = [], []
            for x, y in cent:
                cell_x.append(x)
                cell_y.append(y)
            self.data.obs["cell_x"] = cell_x
            self.data.obs["cell_y"] = cell_y
        else:
            self.data.obs.rename(
                columns={self.cell_x_key: "cell_x", self.cell_y_key: "cell_y"}
            )

    def get_db_table(self):
        self.roi_id()
        self.cell_x_y()
        # Handle statistics
        cell_components_types = []
        cell_components_data = []

        cell_density_types = []
        cell_density_data = []

        cci_types = []
        cci_data = []
        # Cell components
        if self.meta.has_cell_type:
            cell_components = (
                self.cell_components_tb.groupby("type")
                .sum()
                .reset_index()[["type", "value"]]
            )
            cell_components_types = cell_components["type"].tolist()
            cell_components_data = cell_components["value"].tolist()
            # Cell density
            for t, g in self.cell_density_tb.groupby("type"):
                cell_density_types.append(t)
                cell_density_data.append(list(g["value"]))
            # Cell interaction
            cci = self.cell_interaction_tb
            cci_types = pd.unique([*cci["type1"].unique(), *cci["type2"].unique()])
            for t, g in cci.groupby(["type1", "type2"]):
                counts = {0: 0, 1: 0, -1: 0, **Counter(g["value"])}
                roi_sum = sum(list(counts.values()))
                if counts[1] > counts[-1]:
                    value = counts[1] / roi_sum
                else:
                    value = counts[-1] / roi_sum
                if value > 0:
                    cci_data.append([*t, value])
        # Co expression
        co_exp = self.co_expression_tb
        co_exp_markers = pd.unique(
            [*co_exp["marker1"].unique(), *co_exp["marker2"].unique()]
        )
        co_exp_data = co_exp[["marker1", "marker2", "corr"]].to_numpy().tolist()

        # cell info
        roi_id = []
        data_id = []
        cell_x = []
        cell_y = []
        cell_type = []
        cell_name = []
        neighbor_one = []
        neighbor_two = []

        # cell exp
        data_id_exp = []
        roi_id_exp = []
        marker_exp = []
        markers = []
        expression = []

        data_markers = self.data.var[self.markers_key].tolist()
        for n, roi in self.data.obs.groupby("roi_id"):
            # cell info
            roi_id.append(n)
            data_id.append(self.data_id)
            cell_x.append(roi["cell_x"].tolist())
            cell_y.append(roi["cell_y"].tolist())
            cell_name.append(roi[st.CONFIG.neighbors_ix_key].tolist())
            neigh_ones = []
            neigh_twos = []
            for cent, neigh in zip(
                roi[st.CONFIG.neighbors_ix_key], roi[st.CONFIG.NEIGHBORS_KEY]
            ):
                for c in neigh:
                    if c > cent:
                        neigh_ones.append(cent)
                        neigh_twos.append(c)
            neighbor_one.append(neigh_ones)
            neighbor_two.append(neigh_twos)
            if self.meta.has_cell_type:
                cell_type.append(roi["cell_type"].tolist())
            else:
                cell_type.append([])
            markers.append(data_markers)

            # cell exp
            expression += self.data[self.data.obs["roi_id"] == n].X.copy().T.tolist()
            marker_exp += data_markers
            data_id_exp += [self.data_id for _ in range(len(data_markers))]
            roi_id_exp += [n for _ in range(len(data_markers))]

        self.DataRecord = self.meta.to_tb()
        self.DataStats = pd.DataFrame(
            {
                "data_id": self.data_id,
                "cell_components": ujson.dumps(
                    {
                        "data_id": self.data_id,
                        "cell_types": cell_components_types,
                        "components": cell_components_data,
                    }
                ),
                "cell_density": ujson.dumps(
                    {
                        "data_id": self.data_id,
                        "cell_types": cell_density_types,
                        "density": cell_density_data,
                    }
                ),
                "co_expression": ujson.dumps(
                    {
                        "data_id": self.data_id,
                        "markers": co_exp_markers,
                        "relationship": co_exp_data,
                    }
                ),
                "cell_interaction": ujson.dumps(
                    {
                        "data_id": self.data_id,
                        "cell_types": cci_types,
                        "relationship": cci_data,
                    }
                ),
            },
            index=[0],
        )
        self.CellInfo = pd.DataFrame(
            {
                "roi_id": roi_id,
                "data_id": data_id,
                "cell_x": cell_x,
                "cell_y": cell_y,
                "cell_type": cell_type,
                "cell_name": cell_name,
                "neighbor_one": neighbor_one,
                "neighbor_two": neighbor_two,
                "markers": markers,
            }
        )
        self.CellExp = pd.DataFrame(
            {
                "roi_id": roi_id_exp,
                "data_id": data_id_exp,
                "marker": marker_exp,
                "expression": expression,
            }
        )
        self.ROIInfo = pd.DataFrame(
            {
                "roi_id": self.roi_meta["roi_id"].tolist(),
                "data_id": [self.data_id for _ in range(len(self.roi_meta))],
                "header": [
                    self.roi_meta.columns.tolist()[0:-2]
                    for _ in range(len(self.roi_meta))
                ],
                "meta": [
                    [str(x) for x in i]
                    for i in self.roi_meta[["roi_id"] + self.groups_keys]
                    .to_numpy()
                    .tolist()
                ],
                "shannon_entropy": self.roi_meta["shannon_entropy"].tolist(),
                "altieri_entropy": self.roi_meta["altieri_entropy"].tolist(),
            }
        )

    def to_static(self, export=None, static=False, zipped=True):
        if export is not None:
            if isinstance(export, str):
                export = Path(export)
            self.export = export

        export = self.export / self.data_id
        export_zip = self.export / f"{self.data_id}.zip"
        try:
            os.mkdir(export)
        except FileExistsError:
            pass
        data_meta_path = export / "meta.txt"
        cell_info_path = export / "cell_info.txt"
        cell_expression_path = export / "cell_expression.txt"
        # records
        self.DataRecord.to_csv(data_meta_path, sep="\t", index=False)
        # Meta, X, Y, and cell types
        if self.meta.has_cell_type:
            columns = ["cell_type", "cell_x", "cell_y", *self.groups_keys]
        else:
            columns = ["cell_x", "cell_y", *self.groups_keys]
        self.data.obs[columns].to_csv(cell_info_path, sep="\t", index=False)
        # exp
        pd.DataFrame(columns=self.data.var[self.markers_key], data=self.data.X).to_csv(
            cell_expression_path, sep="\t", index=False
        )

        data_tables = [data_meta_path, cell_info_path, cell_expression_path]
        if zipped:
            with ZipFile(export_zip, "w") as file:
                for t in data_tables:
                    file.write(t, Path("/".join(t.parts[-2:])))

        if not static:
            try:
                os.remove(export)
            except (FileNotFoundError, PermissionError):
                pass

    def to_db(self, engine=None):
        if engine is not None:
            init_db(engine)
            self.engine = engine
        engine = self.engine

        insert_policy = dict(if_exists="append", index=False)

        self.DataRecord.to_sql(DataRecord.__tablename__, engine, **insert_policy)
        self.DataStats.to_sql(DataStats.__tablename__, engine, **insert_policy)
        self.CellInfo.to_sql(CellInfo.__tablename__, engine, **insert_policy)
        self.ROIInfo.to_sql(ROIInfo.__tablename__, engine, **insert_policy)
        self.CellExp.to_sql(CellExp.__tablename__, engine, **insert_policy)

    def drop_from_db(self, data_id=None):
        if data_id is None:
            data_id = self.data_id
        tables = [DataRecord, DataStats, CellInfo, ROIInfo, CellExp]
        for t in tables:
            self.engine.execute(sqlalchemy.delete(t).where(data_id == data_id))
