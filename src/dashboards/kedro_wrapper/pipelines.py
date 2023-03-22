import typing as tp

import streamlit as st
from kedro.framework.session import KedroSession

from dashboards.kedro_wrapper import context


def execute_pipeline(
    extra_params: dict[str, tp.Any],
    pipeline_name: str,
) -> dict[str, tp.Any]:
    """
    Function organizing pipeline execution
    NOTE: `extra_params` is interface to parameterize kedro
    pipelines from UI without setting up values

    extra_params (dict[str, tp.Any]): kedro parameters, pass some or all
    pipeline_name (str): a registered pipeline

    Returns:
        dict[str, tp.Any]: _description_
    """
    project_path = context.get_project_dir()
    package = context.get_package_name()
    kedro_session = KedroSession.create(
        package_name=package,
        project_path=project_path,
        extra_params=extra_params,
    )
    output = kedro_session.run(pipeline_name=pipeline_name)
    return output
