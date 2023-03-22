"""Load, read and write data the same way as in kedro catalog session. An extra option list partitions"""

import logging
import typing as tp

import pandas as pd  # noqa: I201
import streamlit as st  # noqa: I201
from kedro.io import DataSetError

logger = logging.getLogger(__name__)


def load_full_partition(dataset):
    try:
        files = load(dataset)
    except DataSetError as error:
        if "No partitions found in" in str(error):
            logger.info(f"DataSetError: {str(error)}")
            files = None
        else:
            logger.error(f"DataSetError: {str(error)}")
            raise DataSetError(str(error))
    return files


def load(
    dataset: str,
    key: str | None = None,
) -> tp.Any:
    catalog = st.session_state["kedro"]["catalog"]
    data = catalog.load(dataset)
    logger.info(f"Loading from catalog source registry: `{dataset}` with key `{key}`")
    if key is not None:
        data = data[key]()
    return data


def list_partition(
    dataset: str,
) -> list:
    logging.info(f"Listing partitions: `{dataset}`")
    files = load_full_partition(dataset)
    if files is None:
        return []
    else:
        return list(files.keys())


def save(
    dataset: str,
    data: tp.Any,
    key: str | None = None,
):
    catalog = st.session_state["kedro"]["catalog"]
    if key is not None:
        data = {key: data}
    data = catalog.save(dataset, data)
    logger.info(f"Saved data: `{dataset}` with key `{key}`")
