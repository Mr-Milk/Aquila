import json
from typing import List, Optional

from crossref.restful import Works

from .utils import formalize, formalize_markers, get_data_id, if_default


class RecordMeta:
    _data_id: str = ""
    _technology: List[str] = [""]
    _species: List[str] = [""]
    _tissue: List[str] = [""]
    _disease: List[str] = [""]
    _disease_subtype: List[str] = [""]
    _molecular: List[str] = [""]
    _markers: List[str] = [""]
    _level_name: List[str] = [""]
    _level_count: List[int] = [""]
    _source_name: List[str] = [""]
    _source_url: List[str] = [""]
    _journal: List[str] = [""]
    _year: List[int] = [""]
    _resolution: List[int] = [""]  # unit: nano meter
    _cell_count: List[int] = [""]
    _marker_count: List[int] = [""]
    _has_cell_type: bool = False

    def __init__(self,
                 doi: Optional[str] = None,
                 data_id: Optional[str] = None,
                 ):
        if doi is not None:
            r = Works()
            result = r.doi(doi)
            self.data_id = result['DOI']
            self.source_url = result['URL']
            self.journal = result['container-title']
            self.source_name = result['title']
            self.year = int(result['published-print']['date-parts'][0][0])

        if data_id is not None:
            self.data_id = data_id

        if (doi is None) & (data_id is None):
            raise ValueError("Please either specific a `doi` or `data_id`.")

    def set(self, **config):
        for k, v in config.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise AttributeError(f"Property {k} not exist")

    def to_json(self, force: bool = False):
        meta = {}
        attrs = ["technology",
                 "resolution",
                 "species",
                 "tissue",
                 "disease",
                 "disease_subtype",
                 "markers",
                 "molecular",
                 "source_name",
                 "source_url",
                 "journal",
                 "year",
                 "level_name",
                 "level_count",
                 "cell_count",
                 "marker_count",
                 ]
        for attr in attrs:
            meta[attr] = if_default(attr, getattr(self, attr), default=[""], ignore=force)
        meta["data_id"] = if_default("data_id", self.data_id, default="", ignore=force)
        meta["has_cell_type"] = self.has_cell_type
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
        if isinstance(value, str):
            value = [value]
        elif isinstance(value, List):
            value = [str(i) for i in value]
        else:
            raise TypeError("Expected str")
        self._technology = value

    @species.setter
    def species(self, value):
        self._species = formalize(value)

    @tissue.setter
    def tissue(self, value):
        self._tissue = formalize(value)

    @disease.setter
    def disease(self, value):
        self._disease = formalize(value)

    @disease_subtype.setter
    def disease_subtype(self, value):
        self._disease_subtype = formalize(value)

    @molecular.setter
    def molecular(self, value):
        ACCEPT = ['RNA', 'DNA', 'Protein', 'Metabolite']
        if isinstance(value, str):
            value = [value]
        elif isinstance(value, List):
            value = [str(i) for i in value]
        for i in value:
            if i not in ACCEPT:
                raise ValueError("Available options are 'RNA', 'DNA', 'Protein' and 'Metabolite'.")
        self._molecular = value

    @markers.setter
    def markers(self, value):
        self._markers = formalize_markers(value)
        self.marker_count = len(self._markers)

    @level_name.setter
    def level_name(self, value):
        self._level_name = formalize(value)

    @level_count.setter
    def level_count(self, value):
        self._level_count = formalize(value)

    @source_name.setter
    def source_name(self, value):
        self._source_name = formalize(value)

    @source_url.setter
    def source_url(self, value):
        self._source_url = formalize(value)

    @journal.setter
    def journal(self, value):
        self._journal = formalize(value)

    @year.setter
    def year(self, value):
        self._year = formalize(value)

    @resolution.setter
    def resolution(self, value):
        self._resolution = formalize(value)

    @cell_count.setter
    def cell_count(self, value):
        self._cell_count = formalize(value)

    @marker_count.setter
    def marker_count(self, value):
        self._marker_count = formalize(value)

    @has_cell_type.setter
    def has_cell_type(self, value):
        if isinstance(value, bool):
            self._has_cell_type = value
        else:
            raise TypeError("Expected bool")
