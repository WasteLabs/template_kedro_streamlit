"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from . import iris


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = {
        "__default__": iris.create_pipeline(),
        "iris": iris.create_pipeline(),
    }
    return pipelines
