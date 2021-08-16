import os
from ast import literal_eval
from collections import Counter
from pathlib import Path
from typing import List, Optional, Union
from uuid import uuid1
from zipfile import ZipFile

import numpy as np
import pandas as pd
import scanpy as sc
import spatialtis as st
import sqlalchemy
import ujson
from anndata import AnnData, read_h5ad
from sqlalchemy.orm import sessionmaker

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
    spatial_entropy_tb: Optional[pd.DataFrame] = None

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
        file: Path,
        groups_keys: Optional[List[str]] = None,
        cell_type_key: Optional[str] = "cell_type",
        markers_key: Optional[str] = "markers",
        centroid_key: Optional[str] = "centroid",
        cell_x_key: Optional[str] = None,
        cell_y_key: Optional[str] = None,
        verbose: bool = False,
    ):
        self.file = file
        self.data = read_h5ad(file)
        self.groups_keys = groups_keys
        self.cell_type_key = cell_type_key
        self.markers_key = markers_key
        self.centroid_key = centroid_key
        self.cell_x_key = cell_x_key
        self.cell_y_key = cell_y_key
        self.verbose = verbose

        if self.cell_type_key is not None:
            self.data.obs.rename(
                columns={self.cell_type_key: "cell_type"}, inplace=True
            )
            self.cell_type_key = "cell_type"

        self.engine = Global.engine
        self.export = Global.export
        init_db(self.engine)

        Session = sessionmaker()

        Session.configure(bind=self.engine)
        self.session = Session()

    def ok(self, export=None, static=False, zipped=True):
        db_record = self.session.query(DataRecord).filter(DataRecord.data_id == self.data_id).count()
        if (db_record == 0) | ((db_record > 0) & (not Global.skip_exist)):
            self.meta.cell_count, self.meta.marker_count = self.data.shape
            print(
                f"Data record {self.meta.data_id} has {self.meta.cell_count} cells and "
                f"{self.meta.marker_count} markers."
            )
            self.get_db_table()
            self.to_static(export, static, zipped)

            # if the dump process is incomplete, abort and clean from db
            try:
                self.to_db()
            except Exception as e:
                print(e)
                self.drop_from_db()
                self.data.write(self.file)

            print(f"Record {self.data_id} dumped to DB successfully")
        else:
            print(f"Record {self.data_id} already exist")

    def set_meta(self, doi=None, data_id=None, id_suffix=None, **kwargs):
        self.meta = RecordMeta(**kwargs).set_id(doi=doi, data_id=data_id, id_suffix=id_suffix)
        self.data_id = self.meta.data_id
        if self.cell_type_key is not None:
            self.meta.has_cell_type = True
        return self

    def run_analysis(self, expand=5):

        st_kwargs = dict(
            cell_type_key=self.cell_type_key,
            exp_obs=self.groups_keys,
            centroid_key=self.centroid_key,
            marker_key=self.markers_key,
        )
        # st.CONFIG.CELL_TYPE_KEY = self.cell_type_key
        # st.CONFIG.EXP_OBS = self.groups_keys
        # st.CONFIG.CENTROID_KEY = self.centroid_key
        # st.CONFIG.MARKER_KEY = self.markers_key
        st.CONFIG.VERBOSE = self.verbose
        st.CONFIG.PBAR = False

        if not isinstance(self.data.X, np.ndarray):
            self.data.X = self.data.X.toarray()

        if self.meta.molecule.name == "Protein":
            self.data.X = (self.data.X - self.data.X.min()) / (
                self.data.X.max() - self.data.X.min()
            )

        # eliminate NA from array
        self.data.X = np.nan_to_num(self.data.X)

        sc.pp.filter_cells(self.data, min_genes=1)
        sc.pp.filter_genes(self.data, min_cells=100)
        # To eliminate the negative value, we need to transform all the data to positive
        # To preserve the distribution, we scale everything to (0, 1)

        sc.pp.normalize_total(self.data, target_sum=100)
        sc.pp.log1p(self.data)
        sc.pp.highly_variable_genes(self.data, min_mean=0.0125, min_disp=0.5)

        selected_markers = []
        for m, hv in zip(
            self.data.var[self.markers_key], self.data.var.highly_variable
        ):
            if hv:
                selected_markers.append(m)

        self.data.obs = self.data.obs.reset_index(drop=True)

        # iterative find neighbors until NN reach [4.5, 7)
        st.find_neighbors(self.data, expand, count=True, **st_kwargs)
        neighbors_count = self.data.obs.cell_neighbors_count.mean()
        print(f"Current neighbor count {neighbors_count}")

        # st.spatial_co_expression(self.data, use_cell_type=True, selected_markers=selected_markers, corr_cutoff=0.5, **st_kwargs)
        st.utils.df2adata_uns(pd.DataFrame(columns=["marker1", "marker2", "corr", "pvalue"]), self.data, "co_expression")
        print(self.data.uns_keys())
        if self.meta.has_cell_type:
            if self.meta.resolution == -1:
                ratio = 10 ** -4
            else:
                ratio = (
                    self.meta.resolution / 10 ** 6
                )  # The resolution is nanometer, convert to mm
            st.cell_density(self.data, ratio=ratio, **st_kwargs)
            st.cell_components(self.data, **st_kwargs)
            st.spatial_heterogeneity(self.data, method="shannon", export_key="shannon_entropy", **st_kwargs)
            st.spatial_heterogeneity(self.data, method="leibovici", export_key="spatial_entropy", **st_kwargs)
            st.neighborhood_analysis(self.data, order=False, **st_kwargs)

            # self.shannon_entropy_tb.rename(
            #     columns={"heterogeneity": "shannon_entropy"}, inplace=True
            # )
            # self.spatial_entropy_tb.rename(
            #     columns={"heterogeneity": "spatial_entropy"}, inplace=True
            # )
            #
            # # cast entropy tb to be the same types
            # self.shannon_entropy_tb = self.shannon_entropy_tb.astype(object)
            # self.spatial_entropy_tb = self.spatial_entropy_tb.astype(object)
        self.data.write(self.file)
        print(f"Finish analysis on {self.file}")
        return self

    def roi_id(self):
        roi_id = []
        track_ix = []
        for n, df in self.data.obs.groupby(self.groups_keys[-1], sort=False):
            uid = str(uuid1())
            roi_id += [uid for _ in range(len(df))]
            track_ix += list(df.index)
        self.data.obs["roi_id"] = pd.Series(roi_id, index=track_ix)

        self.roi_meta = self.data.obs[["roi_id"] + self.groups_keys].drop_duplicates().reset_index()
        self.roi_meta = self.roi_meta.astype(object)

        if self.meta.has_cell_type:

            self.shannon_entropy_tb = st.get_result(self.data, "shannon_entropy")
            self.spatial_entropy_tb = st.get_result(self.data, "spatial_entropy")
            self.shannon_entropy_tb.rename(
                columns={"heterogeneity": "shannon_entropy"}, inplace=True
            )
            self.spatial_entropy_tb.rename(
                columns={"heterogeneity": "spatial_entropy"}, inplace=True
            )
            self.shannon_entropy_tb = self.shannon_entropy_tb.astype(object)
            self.spatial_entropy_tb = self.spatial_entropy_tb.astype(object)

            merge_key = self.groups_keys[-1]
            self.roi_meta[merge_key] = self.roi_meta[merge_key].astype(str)
            self.shannon_entropy_tb[merge_key] = self.shannon_entropy_tb[merge_key].astype(str)
            self.spatial_entropy_tb[merge_key] = self.spatial_entropy_tb[merge_key].astype(str)

            self.roi_meta = self.roi_meta.merge(
                self.shannon_entropy_tb.merge(
                    self.spatial_entropy_tb, on=self.groups_keys[-1]
                ),
                on=self.groups_keys[-1],
            )
        else:
            self.roi_meta["shannon_entropy"] = 0
            self.roi_meta["spatial_entropy"] = 0

        self.roi_meta = self.roi_meta[['roi_id', 'shannon_entropy', 'spatial_entropy'] + self.groups_keys]
        assert len(self.roi_meta['roi_id']) == len(self.roi_meta['roi_id'].unique())

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

    def get_dbstats(self):
        # Handle statistics
        cell_components_types = []
        cell_components_data = []

        cell_density_types = []
        cell_density_data = []

        cci_types = []
        cci_data = []
        # Cell components
        if self.meta.has_cell_type:
            self.cell_components_tb = st.get_result(self.data, "cell_components")
            cell_components = (
                self.cell_components_tb.groupby("type")
                    .sum()
                    .reset_index()[["type", "value"]]
            )
            cell_components_types = cell_components["type"].tolist()
            cell_components_data = cell_components["value"].tolist()
            # Cell density
            self.cell_density_tb = st.get_result(self.data, "cell_density")
            for t, g in self.cell_density_tb.groupby("type"):
                cell_density_types.append(t)
                cell_density_data.append(list(g["value"]))
            # Cell interaction
            self.cell_interaction_tb = st.get_result(self.data, "neighborhood_analysis")
            cci = self.cell_interaction_tb
            cci_types = pd.unique([*cci["type1"].unique(), *cci["type2"].unique()])
            for t, g in cci.groupby(["type1", "type2"]):
                counts = {0: 0, 1: 0, -1: 0, **Counter(g["value"])}
                roi_sum = sum(list(counts.values()))
                if counts[1] > counts[-1]:
                    value = counts[1] / roi_sum  # association
                else:
                    value = - (counts[-1] / roi_sum)  # avoidance
                cci_data.append([*t, value])
            # Co expression
        self.co_expression_tb = st.get_result(self.data, "co_expression")
        co_exp = self.co_expression_tb
        co_exp_markers = pd.unique(
            [*co_exp["marker1"].unique(), *co_exp["marker2"].unique()]
        ).tolist()
        co_exp_data = co_exp[["marker1", "marker2", "corr"]].to_numpy().tolist()

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

    def get_roiinfo(self):
        self.ROIInfo = pd.DataFrame(
            {
                "roi_id": self.roi_meta["roi_id"].tolist(),
                "data_id": [self.data_id for _ in range(len(self.roi_meta))],
                "header": [
                    ["roi_id"] + self.groups_keys
                    for _ in range(len(self.roi_meta))
                ],
                "meta": [
                    [str(x) for x in i]
                    for i in self.roi_meta[["roi_id"] + self.groups_keys]
                        .to_numpy()
                        .tolist()
                ],
                "shannon_entropy": self.roi_meta["shannon_entropy"].tolist(),
                "spatial_entropy": self.roi_meta["spatial_entropy"].tolist(),
            }
        )

    def get_cell_info_exp(self):
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
                if isinstance(neigh, str):
                    neigh = eval(neigh)
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

    def get_db_table(self):
        self.roi_id()
        self.cell_x_y()

        self.get_dbstats()
        self.get_cell_info_exp()
        self.get_roiinfo()
        self.DataRecord = self.meta.to_tb()



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
