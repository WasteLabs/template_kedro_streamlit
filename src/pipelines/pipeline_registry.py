"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from . import iris
from . import iris_agg


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = {
        "__default__": iris.create_pipeline(),
        "iris": iris.create_pipeline(),
        "iris_agg": iris_agg.create_pipeline(),
    }
    return pipelines
