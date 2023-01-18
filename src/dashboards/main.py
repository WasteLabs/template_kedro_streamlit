import os
import sys

from kedro.framework.startup import bootstrap_project
import streamlit as st  # noqa: I201

PROJECT_DIR = os.getcwd()
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

bootstrap_project(PROJECT_DIR)

from src.dashboards import config  # noqa: I100,I201,E402
from src.dashboards import decorators  # noqa: I100,I201,E402


@decorators.kedro_context_required(
    project_dir=config.PROJECT_DIR,
    project_conf_dir=config.PROJECT_CONF_DIR,
    package_name=config.PROJECT_PACKAGE_NAME,
)
def handler():
    st.markdown(
        "# 📄 Template Kedro streamlit \n"
        "Template project for integration of UI of streamlit to data pipelines.\n"
        "Navigate to `iris_aggregation` page\n",
    )
    parameters = st.session_state["parameters"]
    st.text(
        f'{parameters["dashboards"]["pages"]["main"]["text"]}',
    )


if __name__ == "__main__":
    handler()
