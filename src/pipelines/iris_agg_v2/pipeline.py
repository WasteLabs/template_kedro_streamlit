"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=nodes.factory_agg_params,
                inputs=[
                    "params:agg.agg_columns",
                    "params:agg.agg_params",
                ],
                outputs="agg_params",
                name="factory_agg_parameters",
            ),
            node(
                func=nodes.aggregate_dataset,
                inputs=[
                    "params:iris_dataset",
                    "params:agg.group_columns",
                    "agg_params",
                ],
                outputs="iris_aggregation",
                name="iris_aggregation_pipeline",
            ),
        ],
    )
