import hashlib
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from .guards import Molecule, Species, Tech
from .utils import cap_string, get_doi_info


@dataclass
class RecordMeta:
    molecule: Molecule
    technology: Tech
    species: Species
    tissue: str
    disease: str
    disease_subtype: str
    cell_count: int = 0
    marker_count: int = 0
    has_cell_type: bool = False

    data_id: str = field(default=None)
    source_name: str = field(default=None)
    source_url: str = field(default=None)
    journal: str = field(default=None)
    year: int = field(default=None)
    resolution: int = -1  # unit: nano meter

    def set_id(
        self,
        doi: Optional[str] = None,
        data_id: Optional[str] = None,
        id_suffix: Optional[str] = None,
    ):
        if doi is not None:
            result = get_doi_info(doi)
            h = hashlib.blake2s(digest_size=16)
            h.update(result["doi"].encode())
            self.data_id = h.hexdigest()
            if id_suffix is not None:
                self.data_id += f"-{id_suffix}"
            if self.source_name is None:
                self.source_name = result["source_name"]
            if self.source_url is None:
                self.source_url = result["source_url"]
            if self.journal is None:
                self.journal = result["journal"]
            if self.year is None:
                self.year = result["year"]

        print(f"{self.data_id}, journal: {self.journal}, year: {self.year}\n{self.source_name}")

        if data_id is not None:
            self.data_id = data_id

        if (doi is None) & (data_id is None):
            raise ValueError("Please either specific a `doi` or `data_id`.")
        return self

        # connect to database and check for duplication
        # if engine is not None:
        #     if engine.dialect.has_table(engine, DataRecord):
        #         if self.data_id in [i[0] for i in engine.execute(select(DataRecord.data_id))]:
        #             raise ValueError("Duplicate data_id, try `data_id_suffix=True`")
        # else:
        #     warnings.warn("engine not specific, skip duplication check of data_id", category=Warning)

    def to_tb(self):
        meta = dict(
            data_id=self.data_id,
            technology=self.technology.name,
            species=self.species.name,
            tissue=cap_string(self.tissue),
            disease=cap_string(self.disease),
            disease_subtype=cap_string(self.disease_subtype),
            molecule=self.molecule.name,
            source_name=self.source_name,
            source_url=self.source_url,
            journal=self.journal,
            year=self.year,
            resolution=self.resolution,
            cell_count=self.cell_count,
            marker_count=self.marker_count,
            has_cell_type=self.has_cell_type,
        )
        return pd.DataFrame(meta, index=[0])
