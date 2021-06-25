import re
from typing import List

import pandas as pd
from crossref.restful import Etiquette, Works

info = Etiquette("baize", contact_email="yb97643@um.edu.mo")


def get_data_id(text):
    result = re.sub(r"[^\w]", "", text)
    if result != "":
        return result
    else:
        raise ValueError("Empty")


def cap_string(value):
    if isinstance(value, str):
        value = str(value).lower().capitalize()
    else:
        raise TypeError(f"Expected str, {value}")
    return value


def up_string(value):
    if isinstance(value, str):
        value = str(value).upper()
    else:
        raise TypeError(f"Expected str, {value}")
    return value


def get_protein_ids(protein_names):
    pass


def get_gene_ids(gene_names):
    pass


def get_doi_info(doi: str):
    r = Works(etiquette=info)
    result = r.doi(doi)
    journal = None
    if len(result["container-title"]) > 0:
        journal = result["container-title"][0]
    else:
        journal = result["publisher"]

    year = result["issued"]["date-parts"][0][0]
    if (year is None) | (year == 0):
        try:
            year = result["created"]["date-parts"][0][0]
        except:
            pass

    return dict(
        doi=result["DOI"],
        source_url=result["URL"],
        journal=journal,
        source_name=result["title"][0],
        year=int(year),
    )


def formalize_markers(value):
    if isinstance(value, str):
        value = [value.upper()]
    elif isinstance(value, List):
        value = pd.unique(value).tolist()
        value = [str(i).upper() for i in value]
    else:
        raise TypeError("Expected str")

    value = [re.sub(r"\s", "-", i) for i in value]
    value = [re.sub(r"_", "-", i) for i in value]
    return value


def if_default(attr, value, default=None, ignore=False):
    if value == default:
        if not ignore:
            raise ValueError(f"{attr} not set, pass `force=True` to ignore this error.")
    return value
