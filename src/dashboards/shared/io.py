import logging
import typing as tp

from kedro.io import MemoryDataSet
import pandas as pd  # noqa: I201
import streamlit as st  # noqa: I201


def cache_data(
    memory_registry: str,
    data: tp.Any,
):
    catalog = st.session_state["catalog"]
    catalog.add(
        data_set_name=memory_registry,
        data_set=MemoryDataSet(data),
        replace=True,
    )
    logging.info(f"Caching data to catalog as memory registry to: {memory_registry}")


def retrieve_data(
    source_registry: str,
    memory_registry: str,
) -> pd.DataFrame:
    catalog = st.session_state["catalog"]
    if catalog.exists(memory_registry):
        iris = catalog.load(memory_registry)
        logging.info(f"Loading from catalog memory registry: {memory_registry}")
    else:
        iris = catalog.load(source_registry)
        logging.info(f"Loading from catalog source registry: {source_registry}")
        cache_data(
            memory_registry=memory_registry,
            data=iris.copy(),
        )
    return iris
