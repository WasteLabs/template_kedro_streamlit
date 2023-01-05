import logging
import os

from kedro.config import ConfigLoader
from kedro.framework.context import KedroContext
from kedro.framework.hooks import _create_hook_manager
import streamlit as st  # noqa: I201

# NOTE: config belows are independent from kedro pipelines and catalog
# to allow trunk development. example: we create `iris_agg_v2` and
# only change value of `PIPELINE_IRIS_AGG` respectively,
# what gives us more update flexibility and preservance of old version in case of errors
PROJECT_DIR = os.getcwd()
PROJECT_CONF_DIR = PROJECT_DIR + "/conf"
PROJECT_PACKAGE_NAME = "pipelines"
CATALOG_IRIS_REGISTRY = "example_iris_data"
PIPELINE_IRIS_AGG = "iris_agg"
PIPELINE_IRIS_AGG_OUTPUT = "iris_aggregation"


logger = logging.getLogger(__name__)

logger.info("start application deployment...")
st.set_page_config(layout="wide")
logger.debug(f"PROJECT DIRECTORY: {PROJECT_DIR}")
logger.debug(f"PROJECT CONFIGURATION DIRECTORY: {PROJECT_CONF_DIR}")

logger.info("init kedro configuration loader...")
config_loader = ConfigLoader(conf_source=PROJECT_CONF_DIR)

logger.info("init kedro context loader...")
context = KedroContext(
    package_name="pipelines",
    project_path=PROJECT_DIR,
    config_loader=config_loader,
    hook_manager=_create_hook_manager(),
)

logger.info("unpacking kedro context...")
# Initialization of kedro context at start-up helps
# to parametrize dashboard configuration using
# traditional kedro pipeline parameterization approach
catalog = context.catalog
parameters = context.params  # <= Heart of parameterization dashboard

logger.info("finish application deployment...")
