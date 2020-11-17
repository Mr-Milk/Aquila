import os
from ast import literal_eval
from pathlib import Path
from typing import List, Optional, Union
from uuid import uuid4
from zipfile import ZipFile

import pandas as pd
import spatialtis as st
import sqlalchemy
from anndata import AnnData

from .db import (CellExpression, CellInfo, DataRecord, DataStats, GroupLevel,
                 init_db)
from .meta import RecordMeta


class Record:
    # data_records
    data_records_db: Optional[pd.DataFrame] = None
    data_id: Optional[str] = None

    # data_stats
    data_stats_db: Optional[pd.DataFrame] = None
    cell_components_tb: Optional[pd.DataFrame] = None
    cell_density_tb: Optional[pd.DataFrame] = None
    spatial_distribution_tb: Optional[pd.DataFrame] = None
    entropy_shannon_tb: Optional[pd.DataFrame] = None
    entropy_alteiri_tb: Optional[pd.DataFrame] = None

    # cell_info
    cell_info_tb: Optional[pd.DataFrame] = None
    cell_info_db: Optional[pd.DataFrame] = None

    # cell_expression
    cell_expression_tb: Optional[pd.DataFrame] = None
    cell_expression_db: Optional[pd.DataFrame] = None

    # group_level
    levels_table: Optional[pd.DataFrame] = None
    group_level_db: Optional[pd.DataFrame] = None

    # state
    computed: Optional[bool] = None

    def __init__(self,
                 data: AnnData,
                 record_meta: RecordMeta,
                 groups_keys: Optional[List[str]] = None,
                 cell_type_key: Optional[str] = None,
                 markers_key: Optional[str] = None,
                 centroid_key: Optional[str] = None,
                 cell_x_key: Optional[str] = None,
                 cell_y_key: Optional[str] = None,
                 force: bool = False,
                 engine: Optional[sqlalchemy.engine.Engine] = None,
                 export: Union[Path, str, None] = None,
                 ):
        if engine is not None:
            init_db(engine)
            self.engine = engine

        if export is not None:
            if isinstance(export, str):
                export = Path(export)
            self.export = export

        if cell_type_key is None:
            record_meta.has_cell_type = False
            self.computed = False

        data = data.copy()
        cell_count = len(data)
        cell_id = [str(uuid4()) for _ in range(cell_count)]
        roi_id = []
        for n, df in data.obs.groupby(groups_keys):
            uid = str(uuid4())
            roi_id += [uid for _ in range(len(df))]

        data.obs['cell_id'] = cell_id
        data.obs['roi_id'] = roi_id
        if (cell_x_key is None) | (cell_y_key is None):
            cent = data.obs[centroid_key].tolist()
            elem = cent[0]
            if isinstance(elem, str):
                cent = [literal_eval(c) for c in cent]
            cell_x, cell_y = [], []
            for x, y in cent:
                cell_x.append(x)
                cell_y.append(y)
            data.obs['cell_x'] = cell_x
            data.obs['cell_y'] = cell_y
        else:
            data.obs.rename(columns={cell_x_key: 'cell_x', cell_y_key: 'cell_y'})
        data.obs.rename(columns={cell_type_key: 'cell_type'})

        self.data_id = record_meta.data_id
        self.levels_table = data.obs[['roi_id'] + groups_keys]
        self.cell_info_tb = data.obs[['cell_id', 'cell_x', 'cell_y', 'cell_type', 'roi_id']]

        markers = data.var[markers_key]
        self.cell_expression_tb = pd.DataFrame({
            "cell_id": data.obs['cell_id'],
            "markers": [markers for _ in range(cell_count)],
            "expression": data.X.tolist(),
            "roi_id": data.obs['roi_id'],
        })

        record_meta.markers = markers
        record_meta.cell_count = cell_count
        record_meta.level_name = groups_keys
        record_meta.level_count = [len(pd.unique(c)) for _, c in self.levels_table.iteritems()]

        # make db
        self.data_records_db = pd.DataFrame({
            "data_id": [self.data_id],
            "data_meta": [record_meta.to_json(force=force)]
        })

        self.cell_info_db = self.cell_info_tb.copy(deep=True)
        self.cell_info_db['data_id'] = [self.data_id for _ in range(cell_count)]

        self.cell_expression_db = self.cell_expression_tb.copy(deep=True)
        self.cell_expression_db['data_id'] = [self.data_id for _ in range(cell_count)]

        self.group_level_db = pd.DataFrame({
            "data_id": [self.data_id],
            "levels_table": [self.levels_table.to_json(orient="records", force_ascii=False)],
        })

        if self.computed:
            st.CONFIG.EXP_OBS = groups_keys
            st.CONFIG.CELL_TYPE_KEY = cell_type_key
            st.CONFIG.CENTROID_KEY = centroid_key
            st.CONFIG.MULTI_PROCESSING = True
            self.cell_components_tb = st.cell_components(data, export=False, return_df=True)
            self.cell_density_tb = st.cell_density(data, export=False, return_df=True)
            self.spatial_distribution_tb = st.spatial_distribution(data, export=False, return_df=True)
            self.entropy_shannon_tb = st.spatial_heterogeneity(data, method="shannon", export=False, return_df=True)
            self.entropy_alteiri_tb = st.spatial_heterogeneity(data, method="alteiri", export=False, return_df=True)

            self.data_stats_db = pd.DataFrame({
                "data_id": [self.data_id],
                "cell_components": [self.cell_components_tb.to_json(orient="records", force_ascii=False)],
                "cell_density": [self.cell_density_tb.to_json(orient="records", force_ascii=False)],
                "spatial_distribution": [self.spatial_distribution_tb.to_json(orient="records", force_ascii=False)],
                "entropy_shannon": [self.entropy_shannon_tb.to_json(orient="records", force_ascii=False)],
                "entropy_alteiri": [self.entropy_alteiri_tb.to_json(orient="records", force_ascii=False)]
            })
        else:
            self.data_stats_db = pd.DataFrame({
                "data_id": [self.data_id],
                "cell_components": [""],
                "cell_density": [""],
                "spatial_distribution": [""],
                "entropy_shannon": [""],
                "entropy_alteiri": [""],
            })

    def to_static(self, export=None, static=True, zipped=True):
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
        cell_info_path = export / "cell_info.txt"
        cell_expression_path = export / "cell_expression.txt"
        group_level_path = export / "group_level.txt"
        data_tables = [cell_info_path, cell_expression_path, group_level_path]

        self.cell_info_tb.to_csv(cell_info_path, sep="\t", index=False)
        self.cell_expression_tb.to_csv(cell_expression_path, sep="\t", index=False)
        self.levels_table.to_csv(group_level_path, sep="\t", index=False)

        computed_dir = export / "computed"
        cell_components_path = computed_dir / "cell_components.txt"
        cell_density_path = computed_dir / "cell_density.txt"
        spatial_distribution_path = computed_dir / "spatial_distribution.txt"
        entropy_shannon_path = computed_dir / "entropy_shannon.txt"
        entropy_alteiri_path = computed_dir / "entropy_alteiri.txt"
        computed_tables = [cell_components_path, cell_density_path, spatial_distribution_path,
                           entropy_shannon_path, entropy_alteiri_path]
        if self.computed:
            try:
                os.mkdir(computed_dir)
            except FileExistsError:
                pass
            self.cell_components_tb.to_csv(cell_components_path, sep="\t", index=False)
            self.cell_density_tb.to_csv(cell_density_path, sep="\t", index=False)
            self.spatial_distribution_tb.to_csv(spatial_distribution_path, sep="\t", index=False)
            self.entropy_shannon_tb.to_csv(entropy_shannon_path, sep="\t", index=False)
            self.entropy_alteiri_tb.to_csv(entropy_alteiri_path, sep="\t", index=False)

        if zipped:
            with ZipFile(export_zip, "w") as file:
                for t in data_tables:
                    file.write(t)
                if self.computed:
                    for t in computed_tables:
                        file.write(t)

        if not static:
            try:
                os.remove(export)
            except FileNotFoundError:
                pass

    def to_db(self, engine=None):
        if engine is not None:
            init_db(engine)
            self.engine = engine
        engine = self.engine

        self.data_records_db.to_sql(DataRecord.__tablename__, engine, if_exists="append", index=False)
        self.data_stats_db.to_sql(DataStats.__tablename__, engine, if_exists="append", index=False)
        self.cell_info_db.to_sql(CellInfo.__tablename__, engine, if_exists="append", index=False)
        self.cell_expression_db.to_sql(CellExpression.__tablename__, engine, if_exists="append", index=False)
        self.group_level_db.to_sql(GroupLevel.__tablename__, engine, if_exists="append", index=False)

    def drop_from_db(self, data_id=None):
        if data_id is None:
            data_id = self.data_id
        all_tables = [DataRecord, DataStats, CellInfo, CellExpression, GroupLevel]
        for t in all_tables:
            self.engine.execute(sqlalchemy.delete(t).where(data_id == data_id))
