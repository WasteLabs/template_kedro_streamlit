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
    logger.info(f"Kedro session initiated at {project_dir}")
    st.session_state["kedro"] = {}
    st.session_state["kedro"]["config"] = {}
    st.session_state["kedro"]["config"]["project_dir"] = project_dir
    st.session_state["kedro"]["config"]["project_conf_dir"] = project_dir + "/conf"
    st.session_state["kedro"]["config"]["package_name"] = "pipelines"
    st.session_state["kedro"]["pipelines"] = {}


def bootstrap_kedro_project(project_dir: str | None = None, overwrite=False):
    if "kedro" in st.session_state and overwrite is False:
        logger.info("Kedro session already initiated")
        return None
    if project_dir is None:
        project_dir = os.getcwd()
        logger.info("Project directory not provided, using current working directory")
    logger.info("Initiating project at: %s", project_dir)
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


def initiate_context():
    context = load_context()
    if "catalog" in st.session_state["kedro"]:
        logger.info("Kedro catalog already initiated.")
    else:
        st.session_state["kedro"][
            "catalog_counter"
        ] = 0  # useful to force update cashed functions
        st.session_state["kedro"]["catalog"] = context.catalog
    if "parameters" in st.session_state["kedro"]:
        logger.info("Kedro parameters already initiated")
    else:
        st.session_state["kedro"][
            "parameters_counter"
        ] = 0  # useful to force update cashed functions
        st.session_state["kedro"]["parameters"] = context.params


def start_kedro_session(project_dir: str | None = None):
    bootstrap_kedro_project(project_dir)
    initiate_context()


def reload_parameters():
    logger.info("Reloading Kedro parameters")
    if "parameters" in st.session_state["kedro"]:
        logger.warning("Kedro parameters already initiated and will be overwritten")
        st.session_state["kedro"][
            "parameters_counter"
        ] += 1  # useful to force update cashed functions
    context = load_context()
    st.session_state["kedro"]["parameters"] = context.params


def reload_catalog():
    logger.info("Reloading Kedro parameters")
    if "catalog" in st.session_state["kedro"]:
        logger.warning("Kedro catalog already initiated and will be overwritten")
        st.session_state["kedro"][
            "catalog_counter"
        ] += 1  # useful to force update cashed functions
    context = load_context()
    st.session_state["kedro"]["catalog"] = context.catalog


def reload_context():
    logger.info("Reloading Kedro context")
    reload_parameters()
    reload_catalog()
