import typing as tp

from kedro.framework.session import KedroSession


def execute_pipeline(
        package_name: str,
        project_path: str,
        extra_params: dict[str, tp.Any],
        pipeline_name: str,
) -> dict[str, tp.Any]:
    """
    Function organizing pipeline execution
    NOTE: `extra_params` is interface to parameterize kedro
    pipelines from UI without setting up values
    Args:
        package_name (str): _description_
        project_path (str): _description_
        extra_params (dict[str, tp.Any]): _description_
        pipeline_name (str): _description_

    Returns:
        dict[str, tp.Any]: _description_
    """
    kedro_session = KedroSession.create(
        package_name="pipelines",
        project_path=project_path,
        extra_params=extra_params,
    )
    output = kedro_session.run(pipeline_name=pipeline_name)
    return output
