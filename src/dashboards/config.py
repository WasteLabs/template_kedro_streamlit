import logging
import os

from kedro.config import ConfigLoader
from kedro.framework.context import KedroContext
from kedro.framework.hooks import _create_hook_manager


PROJECT_DIR = os.getcwd()
PROJECT_CONF_DIR = PROJECT_DIR + "/conf"

logger = logging.getLogger(__name__)

logger.info("start application deployment...")
logger.debug(f"PROJECT DIRECTORY: {PROJECT_DIR}")
logger.debug(f"PROJECT CONFIGURATION DIRECTORY: {PROJECT_CONF_DIR}")

logger.info("init kedro configuration loader...")
config_loader = ConfigLoader(conf_source=PROJECT_CONF_DIR)

logger.info("init kedro context loader...")
context = KedroContext(
    package_name="pipelines",
    project_path=PROJECT_CONF_DIR,
    config_loader=config_loader,
    hook_manager=_create_hook_manager(),
)

logger.info("unpacking kedro context...")
# Initialization of kedro context at start-up helps
# to parametrize dashboard configuration using
# traditional kedro pipeline parameterization approach
catalog = context.catalog
parameters = context.params

logger.info("finish application deployment...")
