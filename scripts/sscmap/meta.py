import re
from typing import List, Optional, Union
from crossref.restful import Works


class RecordMeta:
    data_id: str = ""
    technology: List[str] = list()
    species: List[str] = list()
    tissue: List[str] = list()
    disease: List[str] = list()
    disease_subtype: List[str] = list()
    molecular: List[str] = list()
    markers: List[str] = list()
    level_name: List[str] = list()
    level_count: List[int] = list()
    source_name: List[str] = list()
    source_url: List[str] = list()
    journal: List[str] = list()
    year: int = 0
    resolution: int = 0  # unit: nano meter
    cell_count: int = 0
    marker_count: int = 0
    has_cell_type: bool = False

    def __init__(self,
                 doi: Optional[str] = None,
                 data_id: Optional[str] = None,
                 ):
        r = Works()
        result = r.doi(doi)
        self.data_id = f"{doi}"

    def supply(self,
               technology: Union[List[str], str, None] = None,
               disease: Union[List[str], str, None] = None,
               tissue: Union[List[str], str, None] = None,
               disease_subtype: Union[List[str], str, None] = None,
               molecular: Union[List[str], str, None] = None,
               markers: Union[List[str], str, None] = None,
               level_name: Union[List[str], str, None] = None,
               level_count: Union[List[int], int, None] = None,
               source_name: Union[List[str], str, None] = None,
               source_url: Union[List[str], str, None] = None,
               journal: Union[List[str], str, None] = None,
               year: Optional[int] = None,
               resolution: Optional[int] = None,
               cell_count: Optional[int] = None,
               marker_count: Optional[int] = None,
               has_cell_type: Optional[bool] = None,
               ):
        pass

    def _check_completion(self):
        complete = False
        if self.data_id == "":
            complete

    def to_json(self):
        pass
