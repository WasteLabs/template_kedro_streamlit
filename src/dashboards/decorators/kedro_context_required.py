from functools import wraps

import streamlit as st
from kedro.config import ConfigLoader  # noqa: I201,I100
from kedro.framework.context import KedroContext
from kedro.framework.hooks import _create_hook_manager


def kedro_context_required(
        project_dir: str,
        project_conf_dir: str,
        package_name: str,
) -> callable:

    def decorator(page_handler: callable):

        @wraps(page_handler)
        def wrapper(*args, **kwargs):
            if "catalog" not in st.session_state:
                config_loader = ConfigLoader(conf_source=project_conf_dir)
                context = KedroContext(
                    package_name=package_name,
                    project_path=project_dir,
                    config_loader=config_loader,
                    hook_manager=_create_hook_manager(),
                )
                st.session_state["catalog"] = context.catalog
                st.session_state["parameters"] = context.params
            return page_handler(*args, **kwargs)

        return wrapper

    return decorator
