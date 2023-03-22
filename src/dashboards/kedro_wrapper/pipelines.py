import logging
import typing as tp
from copy import deepcopy

import streamlit as st
from kedro.framework.session import KedroSession

from dashboards.kedro_wrapper import catalog, context
from dashboards.kedro_wrapper.params import load, load_all, save

logger = logging.getLogger(__name__)


def execute_pipeline(
    extra_params: dict[str, tp.Any],
    pipeline_name: str,
):
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
    kedro_session.run(pipeline_name=pipeline_name)


class PipelineSession:
    """The idea here is to have one pipeline app. It can be run using multiple kedro files.
    If restarted, it just starts from the session, but then the key will be lost...
    Maybe make this part of streamlit session state?
    """

    def __init__(
        self,
        pipeline_name: str,
        reload: bool = False,
        key: str | None = None,
    ):
        self.key = key
        self.pipeline_name = pipeline_name
        self.parameters_path = "parameters__" + pipeline_name
        if reload is True or self.parameters_path not in st.session_state["kedro"]:
            st.session_state["kedro"][self.parameters_path] = deepcopy(load_all())

    def reset(self):
        """Reset parameters to default"""
        st.session_state["kedro"][self.parameters_path] = deepcopy(load_all())

    def set_key(self, key: str | None):
        """Update key for catalog save"""
        self.key = key

    def get_param(self, param_name: str) -> tp.Any:
        """Get parameter value or values"""
        return load(param_name, self.parameters_path)

    def set_param(self, param_name: str, value: tp.Any):
        """Save parameter value or values"""
        return save(param_name, value, self.parameters_path)

    def params(self):
        """Get all parameters"""
        return st.session_state["kedro"][self.parameters_path]

    def load_params(self, key: str | None = None):
        """Load parameters from catalog"""
        if key is None:
            key = self.key
        params = catalog.load(self.parameters_path, key)
        st.session_state["kedro"][self.parameters_path] = deepcopy(params)

    def save_params(self, key: str | None = None, reload_catalog: bool = True):
        """Save parameters to catalog"""
        if key is None:
            key = self.key
        catalog.save(
            self.parameters_path, self.params(), key, reload_catalog=reload_catalog
        )

    def run(self, key: str | None = None):
        """Run pipeline"""
        if key is None:
            key = self.key
        extra_params = self.params()
        catalog.save(self.parameters_path, extra_params, key, reload_catalog=False)
        execute_pipeline(extra_params, self.pipeline_name)
        context.reload_catalog()

    def list_param_files(self):
        """List available parameter files"""
        return catalog.list_partition(self.parameters_path)


def initiate_pipeline(
    pipeline_name: str,
    reload: bool = False,
    key: str | None = None,
) -> PipelineSession:
    """Initiate pipeline session"""
    if pipeline_name not in st.session_state["kedro"]["pipelines"]:
        st.session_state["kedro"]["pipelines"][pipeline_name] = PipelineSession(
            pipeline_name, reload=reload, key=key
        )
    else:
        logger.info(f"Pipeline {pipeline_name} session already initiated")
    return st.session_state["kedro"]["pipelines"][pipeline_name]


def return_pipeline(
    pipeline_name: str,
) -> PipelineSession:
    """Initiate pipeline session"""
    return st.session_state["kedro"]["pipelines"][pipeline_name]
