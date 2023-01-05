import streamlit as st

from src.dashboards import config  # noqa: I100,I201
from src.shared import runner  # noqa: I100,I201


def handler():
    left, right = st.columns(2, gap="small")
    iris = config.catalog.load(config.CATALOG_IRIS_REGISTRY)
    with left:
        st.dataframe(data=iris)
    with right:
        group_columns = st.multiselect(
            label="Choose grouping columns",
            options=list(iris.columns),
            default=config.parameters["agg"]["group_columns"],
        )
        agg_columns = st.multiselect(
            label="Choose aggregation columns",
            options=list(iris.columns),
            default=config.parameters["agg"]["agg_columns"],
        )
        agg_params = st.multiselect(
            label="Choose aggregation function",
            options=config.parameters["dashboards"]["pages"]["iris_aggregation"]["agg_params"],
            default=config.parameters["agg"]["agg_params"],
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
            },
            pipeline_name=config.PIPELINE_IRIS_AGG,
        )
        aggregated_iris_dataset = aggregated_iris_dataset[config.PIPELINE_IRIS_AGG_OUTPUT]
        st.dataframe(aggregated_iris_dataset)


if __name__ == "__main__":
    handler()
