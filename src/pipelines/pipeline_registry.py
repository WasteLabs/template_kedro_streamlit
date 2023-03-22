"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from . import iris_agg, iris_agg_v2, test


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = {
        "__default__": iris_agg.create_pipeline(),
        "iris_agg": iris_agg.create_pipeline(),
        "iris_agg_v2": iris_agg_v2.create_pipeline(),
        "test": test.create_pipeline(),
    }
    return pipelines
