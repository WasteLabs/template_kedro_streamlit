"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""
from typing import Dict

import pandas as pd

from pipelines.utils.partitioned_data import call_callable


def return_head(data: pd.DataFrame, head_size: int) -> pd.DataFrame:
    return data.head(head_size)


def return_partitioned_head(
    data: pd.DataFrame, head_size, key: str
) -> Dict[str, pd.DataFrame]:
    return {key: data.head(head_size)}
