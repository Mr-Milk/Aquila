from enum import Enum
from pathlib import Path
from typing import Optional, Union

import sqlalchemy
from pyensembl import EnsemblRelease

data = EnsemblRelease(77)


class _Global:
    engine: Optional[sqlalchemy.engine.Engine] = None
    export: Union[Path, str, None] = None


Global = _Global()


class Tech(Enum):
    # protein
    IMC: str = "IMC"
    MIBI: str = "MIBI"
    CODEX: str = "CODEX"

    # RNA or DNA
    MERFISH: str = "MERFISH"
    osmFISH: str = "osmFISH"
    seqFISH: str = "seqFISH"
    seqFISHPlus: str = "seqFISH+"
    GEOseq: str = "GEO-seq"
    LCMseq: str = "LCM-seq"


class Molecule(Enum):
    RNA: str = "RNA"
    DNA: str = "DNA"
    Protein: str = "Protein"
    Metabolite: str = "Metabolite"


class Species(Enum):
    Human: str = "Human"
    Mouse: str = "Mouse"
