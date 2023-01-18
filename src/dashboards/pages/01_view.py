import os
import sys

from kedro.framework.startup import bootstrap_project
import streamlit as st  # noqa: I201

PROJECT_DIR = os.getcwd()
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

bootstrap_project(PROJECT_DIR)

from src.dashboards import config  # noqa: I100,I201,E402
from src.dashboards.shared import io  # noqa: I100,I201,E402


def handler():
    iris = io.retreive_cached_data(
        source_registry=config.CATALOG_IRIS_REGISTRY,
        memory_registry=config.CATALOG_IRIS_INSTANCE,
    )
    st.dataframe(data=iris)


if __name__ == "__main__":
    handler()
