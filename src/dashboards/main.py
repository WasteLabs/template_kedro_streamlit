import os
import sys

from kedro.framework.startup import bootstrap_project
import streamlit as st  # noqa: I201

PROJECT_DIR = os.getcwd()
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

bootstrap_project(PROJECT_DIR)

from src.dashboards.config import parameters  # noqa: E402,I100


if __name__ == "__main__":
    st.markdown(
        "# 📄 Template Kedro streamlit \n"
        "Template project for integration of UI of streamlit to data pipelines.\n"
        "Navigate to `iris_aggregation` page\n",
    )
    st.text(
        f'{parameters["dashboards"]["pages"]["main"]["text"]}',
    )
