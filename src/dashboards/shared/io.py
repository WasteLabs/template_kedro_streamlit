import logging

from kedro.io import MemoryDataSet
import pandas as pd  # noqa: I201
import streamlit as st  # noqa: I201


def retreive_cached_data(
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
        catalog.add(
            data_set_name=memory_registry,
            data_set=MemoryDataSet(iris),
            replace=True,
        )
        logging.info(f"Caching data to catalog as memory registry to: {memory_registry}")
    return iris
