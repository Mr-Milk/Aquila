from enum import Enum

from pyensembl import EnsemblRelease

data = EnsemblRelease(77)


class Tech(Enum):
    # protein
    IMC = "IMC"
    MIBI = "MIBI"
    CODEX = "CODEX"

    # RNA or DNA
    MERFISH = "MERFISH"
    osmFISH = "osmFISH"
    seqFISH = "seqFISH"
    seqFISHPlus = "seqFISH+"
    GEOseq = "GEO-seq"
    LCMseq = "LCM-seq"


class Molecular(Enum):
    RNA = "RNA"
    DNA = "DNA"
    Protein = "Protein"
    Metabolite = "Metabolite"
