import re
from typing import List

import pandas as pd


def get_data_id(text):
    result = re.sub(r'[^\w]', "", text)
    if result != "":
        return result
    else:
        raise ValueError("Empty")


def formalize(value):
    if isinstance(value, List):
        value = [str(i).lower().capitalize() for i in value]
    if isinstance(value, str):
        value = [str(value).lower().capitalize()]
    if isinstance(value, float):
        if value.is_integer():
            value = [int(value)]
        else:
            raise TypeError(f"Your input number has decimal, {value}")
    return value


def formalize_markers(value):
    if isinstance(value, str):
        value = [value.upper()]
    elif isinstance(value, List):
        value = pd.unique(value).tolist()
        value = [str(i).upper() for i in value]
    else:
        raise TypeError("Expected str")

    value = [re.sub(r'\s', "-", i) for i in value]
    return value


def if_default(attr, value, default=None, ignore=False):
    if value == default:
        if not ignore:
            raise ValueError(f"{attr} not set, pass `force=True` to ignore this error.")
    return value
