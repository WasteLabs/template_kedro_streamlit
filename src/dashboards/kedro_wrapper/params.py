"""Load, read and write params. An extra option list partitions"""

import logging
import typing as tp

import streamlit as st  # noqa: I201

logger = logging.getLogger(__name__)


def get_nested_params(input: dict, key: list[str]):
    key_i = key.pop(0)
    if not key:
        return input[key_i]
    else:
        return get_nested_params(input[key_i], key)


def load_all(parameters_path="parameters"):
    logger.info(f"Loading all parameters")
    params = st.session_state["kedro"][parameters_path]
    return params


def load(
    param_name: str,
    parameters_path="parameters",
) -> tp.Any:
    """For nested access, separate `param_name` with `.`"""
    logger.info(f"Loading parameters: `{param_name}`")
    params = st.session_state["kedro"][parameters_path]
    param_path = param_name.split(".")
    value = get_nested_params(params, param_path)
    return value


def set_nested_params(input: dict, key: list[str], value: tp.Any):
    key_i = key.pop(0)
    if not key:
        input[key_i] = value
    else:
        set_nested_params(input[key_i], key, value)


def save(
    param_name: str,
    value: tp.Any,
    parameters_path="parameters",
):
    """For nested access, separate `param_name` with `.`"""
    logger.info(f"Loading parameters: `{param_name}`")
    params = st.session_state["kedro"][parameters_path]
    param_path = param_name.split(".")
    set_nested_params(params, param_path, value)


class ParametersSession:
    def __init__(self, session_name="parameters"):
        self.parameters_path = session_name

    def load(self, param_name: str) -> tp.Any:
        return load(param_name, self.parameters_path)

    def save(self, param_name: str, value: tp.Any):
        return save(param_name, value, self.parameters_path)

    def params(self):
        return st.session_state["kedro"][self.parameters_path]

    def session_save(self):
        st.session_state["kedro"][self.parameters_path] = self.params()

    def session_load(self, key: str | None = None):
        st.session_state["kedro"][self.parameters_path] = self.params()
