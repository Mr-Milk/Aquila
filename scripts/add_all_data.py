from pathlib import Path

import anndata as ad
import spatialtis as st
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sscmap import Global, Molecule, Record, Tech

from scripts.sscmap import Species

config = dotenv_values(".env")
Global.engine = create_engine(
    f"postgres://{config['USER']}:{config['PASSWORD']}"
    f"@{config['HOST']}/{config['DB_NAME']}"
)

Global.export = Path("/Volumes/MILK-SSD/aquila-static")
save_h5ad_path = Path("/Volumes/MILK-SSD/aquila-h5ad-data")

# ========= IMC data ==========
# data = ad.read_h5ad(save_h5ad_path / 'scp.h5ad')
# r = Record(data, groups_keys=['core', 'grade', 'gender', 'age', 'Patientstatus']).set_meta(
#     doi="10.1038/s41586-019-1876-x",
#     technology=Tech.IMC,
#     species=Species.Human,
#     tissue="breast",
#     molecule=Molecule.Protein,
#     disease="cancer",
#     disease_subtype="breast cancer",
#     resolution=1000,
# ).ok(expand=30)
#
# data = ad.read_h5ad(save_h5ad_path / 'covid-imc.h5ad')
# r = Record(data, groups_keys=['roi', 'sample', 'disease', 'phenotypes']).set_meta(
#     doi="10.1038/s41586-021-03475-6",
#     technology=Tech.IMC,
#     species=Species.Human,
#     tissue="lung",
#     molecule=Molecule.Protein,
#     disease="COVID-19",
#     disease_subtype="",
#     resolution=1000,
# ).ok(expand=30)

data = ad.read_h5ad(save_h5ad_path / "imc_data.h5ad")
r = (
    Record(data, groups_keys=["image", "case", "slide", "part", "group", "stage"])
    .set_meta(
        doi="10.1016/j.cmet.2018.11.014",
        technology=Tech.IMC,
        species=Species.Human,
        molecule=Molecule.Protein,
        tissue="pancreas",
        disease="diabetes",
        disease_subtype="Type 1 diabetes",
        resolution=1000,
    )
    .ok(expand=13)
)

data = ad.read_h5ad(save_h5ad_path / "IMC-multiomic-breast-cancer.h5ad")
r = (
    Record(data, groups_keys=["ROI", "METABRIC_ID"])
    .set_meta(
        doi="10.1038/s43018-020-0026-6",
        technology=Tech.IMC,
        species=Species.Human,
        molecule=Molecule.Protein,
        tissue="breast",
        disease="cancer",
        disease_subtype="breast cancer",
        resolution=1000,
    )
    .ok(expand=13)
)

data = ad.read_h5ad(save_h5ad_path / "IMC-multiple-sclerosis-lesions.h5ad")
r = (
    Record(data, groups_keys=["ROI", "Part"])
    .set_meta(
        doi="10.7554/eLife.48051",
        technology=Tech.IMC,
        species=Species.Human,
        molecule=Molecule.Protein,
        tissue="brain",
        disease="Multiple sclerosis lesions",
        disease_subtype="",
        resolution=1000,
    )
    .ok(expand=13)
)

# ========= MIBI data =============
data = ad.read_h5ad(save_h5ad_path / "mibi_TNBC_data.h5ad")
r = (
    Record(data, groups_keys=["Patient", "Stage"])
    .set_meta(
        doi="10.1016/j.cell.2018.08.039",
        technology=Tech.MIBI,
        species=Species.Human,
        tissue="breast",
        molecule=Molecule.Protein,
        disease="cancer",
        disease_subtype="breast cancer",
        resolution=260,
    )
    .ok(expand=30)
)

data = ad.read_h5ad(save_h5ad_path / "codex_spleen.h5ad")
r = (
    Record(data, groups_keys=["ROI"])
    .set_meta(
        doi="10.1016/j.cell.2018.07.010",
        technology=Tech.CODEX,
        species=Species.Mouse,
        tissue="spleen",
        molecule=Molecule.Protein,
        disease="autoimmune",
        disease_subtype="lupus",
        resolution=188,
    )
    .ok(expand=30)
)

data = ad.read_h5ad("data/seqFISH-OB.h5ad")
r = (
    Record(data, groups_keys=["FOV"], markers_key="markers", centroid_key="centroid",)
    .set_meta(
        doi="https://doi.org/10.1038/s41586-019-1049-y",
        technology=Tech.seqFISH,
        tissue="olfactory bulb",
        molecular=Molecule.RNA,
        disease="",
        disease_subtype="",
    )
    .ok(expand=130)
)
