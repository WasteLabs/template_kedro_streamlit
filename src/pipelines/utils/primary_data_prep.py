import logging
from typing import Dict, List

import pandas as pd

log = logging.getLogger(__name__)


def check_unique_ids(data, id_columns):
    for column in id_columns:
        duplicates = data[column].duplicated(keep=False)
        if duplicates.any():
            error_str = f"{duplicates.sum()} duplicates found in `{column}`:\n{data.loc[duplicates]}"
            log.error(error_str)
            raise ValueError(error_str)


def create_duplicates(
    data: pd.DataFrame, duplicate_columns: Dict[str, str]
) -> pd.DataFrame:
    for col in duplicate_columns:
        data = data.assign(**{duplicate_columns[col]: data[col]})
    return data


def create_id_categories(data: pd.DataFrame, id_columns: List[str]):
    type_change = {x: "category" for x in id_columns}
    return data.astype(type_change)
