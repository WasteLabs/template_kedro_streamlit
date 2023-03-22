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
        if key_i not in input:
            input[key_i] = {}
        create_nested_params(input[key_i], key, value)


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


def create_nested_params(params: dict, key: list[str], value: tp.Any):
    key_i = key.pop(0)
    if not key:
        params[key_i] = value
    else:
        if key_i not in params:
            params[key_i] = {}
        create_nested_params(params[key_i], key, value)
