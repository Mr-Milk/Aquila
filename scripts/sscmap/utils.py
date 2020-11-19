import re
from typing import List

import pandas as pd


def get_data_id(text):
    result = re.sub(r'[^\w]', "", text)
    if result != "":
        return result
    else:
        raise ValueError("Empty")


def formalize_str(value):
    if isinstance(value, str):
        value = str(value).lower().capitalize()
    else:
        raise TypeError(f"Expected str, {value}")
    return value


def formalize_uint(value):
    if isinstance(value, str):
        try:
            value = float(value)
        except TypeError:
            raise TypeError(f"Expected a number, {value}")

    elif isinstance(value, float):
        if value < 0:
            raise ValueError(f"Your input number is negative, {value}")
        elif value.is_integer():
            value = int(value)
        else:
            raise TypeError(f"Your input number has decimal, {value}")
    elif isinstance(value, int):
        if value < 0:
            raise ValueError(f"Your input number is negative, {value}")
    else:
        raise TypeError(f"Expected a number, {value}")
    return value


def formalize_list_uint(value):
    if isinstance(value, List):
        if len(value) == 0:
            raise ValueError("Empty list")
        new_value = []
        for i in value:
            i = formalize_uint(i)
            new_value.append(i)
        value = new_value
    elif isinstance(value, (int, float)):
        value = formalize_uint(value)
    else:
        raise TypeError("Expected a list of positive int")

    return value


def formalize_list_str(value):
    if isinstance(value, List):
        if len(value) == 0:
            raise ValueError("Empty list")
        new_value = []
        for i in value:
            i = formalize_str(i)
            new_value.append(i)
        value = new_value
    elif isinstance(value, str):
        value = [value]
    else:
        raise TypeError("Expected a list of str")
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
    value = [re.sub(r'_', "-", i) for i in value]
    return value


def if_default(attr, value, default=None, ignore=False):
    if value == default:
        if not ignore:
            raise ValueError(f"{attr} not set, pass `force=True` to ignore this error.")
    return value
