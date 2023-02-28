import logging
import os

import streamlit as st  # noqa: I201

# NOTE: config belows are independent from kedro pipelines and catalog
# to allow trunk development. example: we create `iris_agg_v2` and
# only change value of `PIPELINE_IRIS_AGG` respectively,
# what gives us more update flexibility and preservance of old version in case of errors
PROJECT_DIR = os.getcwd()
PROJECT_CONF_DIR = PROJECT_DIR + "/conf"
PROJECT_PACKAGE_NAME = "pipelines"
CATALOG_IRIS_REGISTRY = "example_iris_data"
PIPELINE_IRIS_AGG = "iris_agg_v2"
PIPELINE_IRIS_AGG_INPUT = "iris_dataset"
PIPELINE_IRIS_AGG_OUTPUT = "iris_aggregation"
CATALOG_IRIS_INSTANCE = "instance"

logger = logging.getLogger(__name__)

logger.info("start application deployment...")
logger.debug(f"PROJECT DIRECTORY: {PROJECT_DIR}")
logger.debug(f"PROJECT CONFIGURATION DIRECTORY: {PROJECT_CONF_DIR}")

logger.info("finish application deployment...")
