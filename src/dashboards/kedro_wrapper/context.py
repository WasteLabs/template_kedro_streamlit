import logging
import os
import sys
from functools import wraps

import streamlit as st  # noqa: I201
from kedro.config import ConfigLoader  # noqa: I201,I100
from kedro.framework.context import KedroContext
from kedro.framework.hooks import _create_hook_manager
from kedro.framework.startup import bootstrap_project

logger = logging.getLogger(__name__)


def get_project_dir() -> str:
    return st.session_state["kedro"]["config"]["project_dir"]


def get_project_conf_dir() -> str:
    return st.session_state["kedro"]["config"]["project_conf_dir"]


def get_package_name() -> str:
    return st.session_state["kedro"]["config"]["package_name"]


def create_config(project_dir: str):
    if "kedro" in st.session_state:
        logger.warning("Kedro session already initiated and will be overwritten")
    logger.warning(f"Kedro session initiated with path {project_dir}")
    st.session_state["kedro"] = {}
    st.session_state["kedro"]["config"] = {}
    st.session_state["kedro"]["config"]["project_dir"] = project_dir
    st.session_state["kedro"]["config"]["project_conf_dir"] = project_dir + "/conf"
    st.session_state["kedro"]["config"]["package_name"] = "pipelines"


def bootstrap_kedro_project(project_dir: str | None = None):
    if project_dir is None:
        project_dir = os.getcwd()
        logger.info("Project directory not provided, using current working directory")
    logger.info("Initiating project with at: %s", project_dir)
    if project_dir not in sys.path:
        sys.path.append(project_dir)
    bootstrap_project(project_dir)
    create_config(project_dir)


def load_context():
    project_dir = get_project_dir()
    project_conf_dir = get_project_conf_dir()
    package_name = get_package_name()
    config_loader = ConfigLoader(conf_source=project_conf_dir)
    context = KedroContext(
        package_name=package_name,
        project_path=project_dir,
        config_loader=config_loader,
        hook_manager=_create_hook_manager(),
    )
    return context


def initiate_context(reload: bool = False):
    context = load_context()
    if "catalog" in st.session_state["kedro"] and not reload:
        logger.info("Kedro catalog already initiated")
    else:
        st.session_state["kedro"]["catalog"] = context.catalog
    if "parameters" in st.session_state["parameters"] and not reload:
        logger.info("Kedro parameters already initiated")
    else:
        st.session_state["kedro"]["parameters"] = context.params


def start_kedro_session(project_dir: str | None = None):
    bootstrap_kedro_project(project_dir)
    initiate_context(reload=True)


def reload_context():
    logger.info("Reloading Kedro context")
    if "catalog" in st.session_state["kedro"]:
        logger.warning("Kedro catalog already initiated and will be overwritten")
    if "parameters" in st.session_state["kedro"]:
        logger.warning("Kedro parameters already initiated and will be overwritten")
    initiate_context(reload=True)
