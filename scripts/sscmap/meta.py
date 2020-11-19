import json
import warnings
from typing import List, Optional
from uuid import uuid4

import sqlalchemy
from crossref.restful import Works
from sqlalchemy import select

from .db import DataRecord
from .utils import (formalize_list_str, formalize_list_uint, formalize_markers,
                    formalize_str, formalize_uint, get_data_id, if_default)


class RecordMeta:
    _data_id: str = ""
    _technology: str = ""
    _species: str = ""
    _tissue: str = ""
    _disease: str = ""
    _disease_subtype: str = ""
    _molecular: str = ""
    _markers: List[str] = [""]
    _level_name: List[str] = [""]
    _level_count: List[int] = [0]
    _source_name: str = ""
    _source_url: List[str] = [""]
    _journal: str = ""
    _year: int = 0
    _resolution: int = 0  # unit: nano meter
    _cell_count: int = 0
    _marker_count: int = 0
    _has_cell_type: bool = False

    def __init__(self,
                 doi: Optional[str] = None,
                 data_id: Optional[str] = None,
                 data_id_suffix: bool = False,
                 engine: Optional[sqlalchemy.engine.Engine] = None,
                 ):
        if doi is not None:
            r = Works()
            result = r.doi(doi)
            self.data_id = result['DOI']
            self.source_url = result['URL']
            self.journal = result['container-title'][0]
            self.source_name = result['title'][0]
            self.year = int(result['published-print']['date-parts'][0][0])

        if data_id is not None:
            self.data_id = data_id

        if (doi is None) & (data_id is None):
            raise ValueError("Please either specific a `doi` or `data_id`.")

        if data_id_suffix:
            self.data_id += f"-{str(uuid4())[:8]}"

        # connect to database and check for duplication
        if engine is not None:
            if engine.dialect.has_table(engine, DataRecord):
                if self.data_id in [i[0] for i in engine.execute(select(DataRecord.data_id))]:
                    raise ValueError("Duplicate data_id, try `data_id_suffix=True`")
        else:
            warnings.warn("engine not specific, skip duplication check of data_id", category=Warning)

    def set(self, **config):
        for k, v in config.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise AttributeError(f"Property {k} not exist")

    def to_json(self, force: bool = False):
        meta = {}
        attrs = [
            "data_id",
            "technology",
            "species",
            "tissue",
            "disease",
            "disease_subtype",
            "markers",
            "molecular",
            "source_name",
            "source_url",
            "journal",
            "level_name",
            "year",
            "resolution",
            "level_count",
            "cell_count",
            "marker_count",
            "has_cell_type"
        ]
        for attr in attrs:
            meta[attr] = if_default(attr, getattr(self, attr), default=getattr(RecordMeta, attr), ignore=force)
        assert len(self.level_name) == len(self.level_count)
        return json.dumps(meta)

    @property
    def data_id(self):
        return self._data_id

    @property
    def technology(self):
        return self._technology

    @property
    def species(self):
        return self._species

    @property
    def tissue(self):
        return self._tissue

    @property
    def disease(self):
        return self._disease

    @property
    def disease_subtype(self):
        return self._disease_subtype

    @property
    def molecular(self):
        return self._molecular

    @property
    def markers(self):
        return self._markers

    @property
    def level_name(self):
        return self._level_name

    @property
    def level_count(self):
        return self._level_count

    @property
    def source_name(self):
        return self._source_name

    @property
    def source_url(self):
        return self._source_url

    @property
    def journal(self):
        return self._journal

    @property
    def year(self):
        return self._year

    @property
    def resolution(self):
        return self._resolution

    @property
    def cell_count(self):
        return self._cell_count

    @property
    def marker_count(self):
        return self._marker_count

    @property
    def has_cell_type(self):
        return self._has_cell_type

    @data_id.setter
    def data_id(self, value):
        self._data_id = get_data_id(value)

    @technology.setter
    def technology(self, value):
        self._technology = str(value)

    @species.setter
    def species(self, value):
        self._species = formalize_str(value)

    @tissue.setter
    def tissue(self, value):
        self._tissue = formalize_str(value)

    @disease.setter
    def disease(self, value):
        self._disease = formalize_str(value)

    @disease_subtype.setter
    def disease_subtype(self, value):
        self._disease_subtype = formalize_str(value)

    @molecular.setter
    def molecular(self, value):
        ACCEPT = ['RNA', 'DNA', 'Protein', 'Metabolite']
        if value not in ACCEPT:
            raise ValueError("Available options are 'RNA', 'DNA', 'Protein' and 'Metabolite'.")
        self._molecular = value

    @markers.setter
    def markers(self, value):
        self._markers = formalize_markers(value)
        self.marker_count = len(self._markers)

    @level_name.setter
    def level_name(self, value):
        self._level_name = formalize_list_str(value)

    @level_count.setter
    def level_count(self, value):
        self._level_count = formalize_list_uint(value)

    @source_name.setter
    def source_name(self, value):
        self._source_name = formalize_str(value)

    @source_url.setter
    def source_url(self, value):
        self._source_url = formalize_list_str(value)

    @journal.setter
    def journal(self, value):
        self._journal = formalize_str(value)

    @year.setter
    def year(self, value):
        self._year = formalize_uint(value)

    @resolution.setter
    def resolution(self, value):
        self._resolution = formalize_uint(value)

    @cell_count.setter
    def cell_count(self, value):
        self._cell_count = formalize_uint(value)

    @marker_count.setter
    def marker_count(self, value):
        self._marker_count = formalize_uint(value)

    @has_cell_type.setter
    def has_cell_type(self, value):
        if isinstance(value, bool):
            self._has_cell_type = value
        else:
            raise TypeError("Expected bool")
