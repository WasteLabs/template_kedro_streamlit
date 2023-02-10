import os
import sys
import typing as tp

from kedro.framework.startup import bootstrap_project
import pandas as pd  # noqa: I201
from st_aggrid import AgGrid  # noqa: I201
from st_aggrid import GridOptionsBuilder  # noqa: I201
from st_aggrid import GridUpdateMode  # noqa: I201
import streamlit as st  # noqa: I201

PROJECT_DIR = os.getcwd()
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

bootstrap_project(PROJECT_DIR)

from src.dashboards import config  # noqa: I100,I201,E402
from src.dashboards import decorators  # noqa: I100,I201,E402
from src.dashboards.shared import io  # noqa: I100,I201,E402


def _render_editable_table(iris: pd.DataFrame, conf: dict[str, tp.Any]):
    gb = GridOptionsBuilder.from_dataframe(iris)
    # gb.configure_selection(**conf["configure_selection"])
    gb.configure_pagination(**conf["configure_pagination"])
    gb.configure_side_bar(**conf["configure_side_bar"])

    columns = conf["configure_column"]
    gb.configure_column(**columns["sepal_length"])
    gb.configure_column(**columns["sepal_width"])
    gb.configure_column(**columns["petal_length"])
    gb.configure_column(**columns["petal_width"])
    gb.configure_column(**columns["species"])

    gridOptions = gb.build()

    grid_response = AgGrid(
        data=iris,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        **conf["AgGrid"],
    )
    return grid_response


def _get_edited_table(aggird_table: pd.DataFrame):
    return pd.DataFrame(aggird_table["data"])


@decorators.kedro_context_required(
    project_dir=config.PROJECT_DIR,
    project_conf_dir=config.PROJECT_CONF_DIR,
    package_name=config.PROJECT_PACKAGE_NAME,
)
def handler():
    iris = io.retrieve_data(
        source_registry=config.CATALOG_IRIS_REGISTRY,
        memory_registry=config.CATALOG_IRIS_INSTANCE,
    )
    table_configs = st.session_state["parameters"]["dashboards"]["pages"]["edit"]
    is_pressed_update = st.button(label="Update table content")
    aggrid_table = _render_editable_table(iris=iris, conf=table_configs)

    if is_pressed_update:
        edited_table = _get_edited_table(aggrid_table)
        io.cache_data(
            memory_registry=config.CATALOG_IRIS_INSTANCE,
            data=edited_table,
        )


if __name__ == "__main__":
    handler()
