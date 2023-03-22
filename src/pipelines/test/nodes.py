"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""
from typing import Dict

import pandas as pd

from pipelines.utils.partitioned_data import call_callable


def return_head(data: pd.DataFrame) -> pd.DataFrame:
    return data.head()


def return_partitioned_head(
    data: Dict[str, pd.DataFrame], key: str
) -> Dict[str, pd.DataFrame]:
    return {key: call_callable(data[key]).head()}
