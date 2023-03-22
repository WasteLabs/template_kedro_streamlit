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
                func=nodes.return_head,
                inputs=[
                    "example_iris_data",
                ],
                outputs="example_iris_data_head",
                name="return_head",
            ),
            node(
                func=nodes.return_partitioned_head,
                inputs=["example_iris_data", "params:session_key"],
                outputs="example_iris_data_head_partitioned",
                name="return_partitioned_head",
            ),
        ],
    )  # type: ignore
