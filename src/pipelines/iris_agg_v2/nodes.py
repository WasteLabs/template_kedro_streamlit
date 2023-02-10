"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""
import pandas as pd


def factory_agg_params(columns: list[str], params: list[str]) -> dict[str, str]:
    agg_params = {}
    for column in columns:
        for param in params:
            agg_params[f"{column}_{param}"] = (column, param)
    return agg_params


def aggregate_dataset(
        df: pd.DataFrame,
        group_cols: list[str],
        agg_params: dict[str, str],
) -> pd.DataFrame:
    aggregates = df \
        .groupby(group_cols) \
        .agg(**agg_params) \
        .reset_index()
    return aggregates
