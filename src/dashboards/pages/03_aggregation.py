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
from src.shared import runner  # noqa: I100,I201,E402
from src.dashboards import decorators  # noqa: I100,I201,E402


@decorators.kedro_context_required(
    project_dir=config.PROJECT_DIR,
    project_conf_dir=config.PROJECT_CONF_DIR,
    package_name=config.PROJECT_PACKAGE_NAME,
)
@decorators.cached_table_required(
    memory_registry=config.CATALOG_IRIS_INSTANCE,
)
def handler():
    left, right = st.columns(2, gap="small")
    iris = io.retrieve_data(
        source_registry=config.CATALOG_IRIS_REGISTRY,
        memory_registry=config.CATALOG_IRIS_INSTANCE,
    )
    with left:
        st.dataframe(data=iris)
    with right:
        parameters = st.session_state["parameters"]
        group_columns = st.multiselect(
            label="Choose grouping columns",
            options=list(iris.columns),
            default=parameters["agg"]["group_columns"],
        )
        agg_columns = st.multiselect(
            label="Choose aggregation columns",
            options=list(iris.columns),
            default=parameters["agg"]["agg_columns"],
        )
        agg_params = st.multiselect(
            label="Choose aggregation function",
            options=parameters["dashboards"]["pages"]["iris_aggregation"]["agg_params"],
            default=parameters["agg"]["agg_params"],
        )
        is_aggregation_triggered = st.button(label="Run data aggregation")

    if is_aggregation_triggered:
        aggregated_iris_dataset = runner.execute_pipeline(
            package_name=config.PROJECT_PACKAGE_NAME,
            project_path=config.PROJECT_DIR,
            extra_params={
                "agg.group_columns": group_columns,
                "agg.agg_columns": agg_columns,
                "agg.agg_params": agg_params,
                config.PIPELINE_IRIS_AGG_INPUT: iris,
            },
            pipeline_name=config.PIPELINE_IRIS_AGG,
        )
        aggregated_iris_dataset = aggregated_iris_dataset[config.PIPELINE_IRIS_AGG_OUTPUT]
        st.dataframe(aggregated_iris_dataset)


if __name__ == "__main__":
    handler()
