from pathlib import Path

import anndata as ad
import pandas as pd
from sqlalchemy import create_engine
from dotenv import dotenv_values
from sscmap import Global, Record, Tech, Molecule, Species, clean_db

config = dotenv_values(".env.remote")
Global.engine = create_engine(f"postgres://{config['USER']}:{config['PASSWORD']}"
                              f"@{config['HOST']}/{config['DB_NAME']}")

Global.export = Path("aquila-static")
save_h5ad_path = Path("aquila-h5ad-data")

header = [
    'h5ad_file', 'cell_type_key', 'centroid_key', 'markers_key', 'group_keys', 'expand', 'doi', 'technology', 'species',
    'tissue', 'molecule',
    'disease', 'disease_subtype', 'resolution', 'suffix', 'meta_kwargs']

cycif_meta_kwargs = {"journal": "eLife", "source_name": "Highly multiplexed immunofluorescence "
                                                        "imaging of human tissues and tumors using t-CyCIF and conventional optical microscopes"}

data = [
    # CODEX data
    ['CODEX-spleen.h5ad', 'cell_type', 'centroid', 'markers', ['ROI'], 5,
     "10.1016/j.cell.2018.07.010", Tech.CODEX, Species.Mouse, "spleen", Molecule.Protein, "autoimmune", "lupus", 188,
     None,
     ],
    ['CODEX-colorectal-cancer.h5ad', 'cell_type', 'centroid', 'markers', ['ROI'], 35,
     "10.1016/j.cell.2020.07.005", Tech.CODEX, Species.Human, "colon", Molecule.Protein, "cancer", "colorectal cancer",
     377, None
     ],

    # CyCIF data
    ['CyCIF-GBM.h5ad', None, 'centroid', 'markers', ["frame"], 25,
     "10.7554/eLife.31657.001", Tech.CyCIF, Species.Human, "brain", Molecule.Protein, "cancer",
     "glioblastoma multiforme", 110, "GBM",
     cycif_meta_kwargs
     ],
    ['CyCIF-PDAC.h5ad', None, 'centroid', 'markers', ["frame"], 20,
     "10.7554/eLife.31657.001", Tech.CyCIF, Species.Human, "pancreas", Molecule.Protein, "cancer",
     "pancreatic ductal adenocarcinoma", 110, "PDAC",
     cycif_meta_kwargs
     ],
    ['CyCIF-TMA.h5ad', None, 'centroid', 'markers',
     ['Anatomic site', 'Age', 'Sex', 'Histology', 'Stage (TNM)', 'image', ], 18,
     "10.7554/eLife.31657.001", Tech.CyCIF, Species.Human, "mixed", Molecule.Protein, "cancer", "mixed", 110, "TMA",
     cycif_meta_kwargs
     ],

    ['CyCIF-tonsil-1.h5ad', None, 'centroid', 'markers', ["frame"], 11,
     "10.1038/s41596-019-0206-y", Tech.CyCIF, Species.Human, "tonsil", Molecule.Protein, "normal", "normal", 200,
     "tonsil-1"],
    ['CyCIF-tonsil-2.h5ad', None, 'centroid', 'markers', ["frame"], 11,
     "10.1038/s41596-019-0206-y", Tech.CyCIF, Species.Human, "tonsil", Molecule.Protein, "normal", "normal", 200,
     "tonsil-2"],
    ['CyCIF-lung.h5ad', None, 'centroid', 'markers', ["metastasis", "frame"], 11,
     "10.1038/s41596-019-0206-y", Tech.CyCIF, Species.Human, "lung", Molecule.Protein, "cancer", "lung cancer", 200,
     "lung"],

    # IMC data
    ['IMC-scp-basel.h5ad', 'cell_type', 'centroid', 'markers', ['Patientstatus', 'age', 'gender', 'grade', 'core'], 15,
     "10.1038/s41586-019-1876-x", Tech.IMC, Species.Human, "breast", Molecule.Protein, "cancer", "breast cancer", 1000,
     "basel",
     ],
    ['IMC-scp-zurich.h5ad', 'cell_type', 'centroid', 'markers', ['age', 'gender', 'grade', 'core'], 15,
     "10.1038/s41586-019-1876-x", Tech.IMC, Species.Human, "breast", Molecule.Protein, "cancer", "breast cancer", 1000,
     "zurich",
     ],
    ['IMC-covid-clean.h5ad', 'metacluster_label', 'centroid', 'markers', ['phenotypes', 'disease', 'sample', 'roi'], 20,
     "10.1038/s41586-021-03475-6", Tech.IMC, Species.Human, "lung", Molecule.Protein, "COVID-19", "COVID-19", 1000,
     None,
     ],
    ['IMC-diabetes.h5ad', 'cell_type', 'centroid', 'markers', ['stage', 'group', 'part', 'slide', 'case', 'image'], 13,
     "10.1016/j.cmet.2018.11.014", Tech.IMC, Species.Human, "pancreas", Molecule.Protein, "diabetes", "Type-1 diabetes",
     1000
     ],
    ['IMC-multiomic-breast-cancer.h5ad', 'cell_type', 'centroid', 'markers', ['ROI'], 16,
     "10.1038/s43018-020-0026-6", Tech.IMC, Species.Human, "breast", Molecule.Protein, "cancer", "breast cancer", 1000,
     None,
     ],
    ['IMC-multiple-sclerosis-lesions.h5ad', 'cell_type', 'centroid', 'markers', ['ROI'], 25,
     "10.7554/eLife.48051", Tech.IMC, Species.Human, "brain", Molecule.Protein, "CNS disorder",
     "Multiple sclerosis lesions", 1000, None,
     ],

    # MIBI data
    ['MIBI-TNBC-new.h5ad', 'cell_type', 'centroid', 'markers', ['patient_class', 'patient'], 30,
     "10.1016/j.cell.2018.08.039", Tech.MIBI, Species.Human, "breast", Molecule.Protein, "cancer", "breast cancer", 260,
     None,
     ],
    ['MIBI-TNBC-survival.h5ad', 'cell_type', 'centroid', 'Biomarker', ['roi'], 30,
     "10.1101/2021.01.06.425496", Tech.MIBI, Species.Human, "breast", Molecule.Protein, "cancer", "breast cancer", 260,
     None,
     ],
    ['MIBI-scMEP.h5ad', 'Cluster', 'centroid', 'markers', ['category', 'donor', 'point'], 30,
     "10.1038/s41587-020-0651-8", Tech.MIBI, Species.Human, "colon", Molecule.Protein, "cancer", "colorectal cancer",
     400, None,
     ],

    # In-situ seq
    ['osmFISH-sscortex.h5ad', 'ClusterName', 'centroid', 'markers', ['Region'], 400,
     "10.1038/s41592-018-0175-z", Tech.osmFISH, Species.Mouse, "somatosensory cortex", Molecule.RNA, "normal", "normal",
     -1, None
     ],

    ['seqFISH-cortex.h5ad', 'cell_type', 'centroid', 'markers', ['Field of View'], 120,
     "10.1038/s41586-019-1049-y", Tech.seqFISH, Species.Mouse, "cortex", Molecule.RNA, "normal", "normal", -1, "cortex"
     ],
    ['seqFISH-ob.h5ad', 'cell_type', 'centroid', 'markers', ['Field of View'], 100,
     "10.1038/s41586-019-1049-y", Tech.seqFISH, Species.Mouse, "olfactory bulb", Molecule.RNA, "normal", "normal", -1,
     "ob"
     ],

    ['MERFISH-cell-cycle.h5ad', None, 'centroid', 'markers', ['ROI'], 180,
     "10.1073/pnas.1912459116", Tech.MERFISH, Species.Human, "U-2 cell", Molecule.RNA, "cancer", "osteosarcoma", -1,
     None,
     ],

    ['MERFISH-hypo-preoptic.h5ad', 'cell_type', 'centroid', 'markers', ['ROI'], 26,
     "10.1126/science.aau5324", Tech.MERFISH, Species.Mouse, "brain", Molecule.RNA, "normal", "normal", -1, None,
     ],

]


for _, record in records.iterrows():
    print(f"\nProcessing {record['h5ad_file']}")
    cell_type_key = None
    has_cell_type = True
    if record['cell_type_key'] is not None:
        cell_type_key = record['cell_type_key']
    else:
        has_cell_type = False
    kw = {}
    if record.get('meta_kwargs') is not None:
        kw = record['meta_kwargs']
    r = Record(save_h5ad_path / record['h5ad_file'],
                groups_keys=record['group_keys'],
                cell_type_key=cell_type_key,
                centroid_key=record['centroid_key'],
                markers_key=record['markers_key'],
          )
    r.set_meta(
                doi=record['doi'],
                technology=record['technology'],
                species=record['species'],
                tissue=record['tissue'],
                molecule=record['molecule'],
                disease=record['disease'],
                disease_subtype=record['disease_subtype'],
                resolution=record['resolution'],
                has_cell_type=has_cell_type,
                id_suffix=record['suffix'],
                **kw,)
    # r.run_analysis(expand=record['expand'])
    r.ok()