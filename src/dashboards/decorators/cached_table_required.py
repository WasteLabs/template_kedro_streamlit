from functools import wraps

import streamlit as st


def cached_table_required(memory_registry: str) -> callable:

    def decorator(page_handler: callable):

        @wraps(page_handler)
        def wrapper(*args, **kwargs):
            catalog = st.session_state["catalog"]
            if catalog.exists(memory_registry):
                page_handler(*args, **kwargs)
            else:
                st.error("cached data is needed, please visit view & edit pages")

        return wrapper

    return decorator
