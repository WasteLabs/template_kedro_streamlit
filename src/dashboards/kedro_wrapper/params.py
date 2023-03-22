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
        get_nested_params(input[key_i], key)


def load(
    param_name: str,
) -> tp.Any:
    """For nested access, separate `param_name` with `.`"""
    logger.info(f"Loading parameters: `{param_name}`")
    params = st.session_state["kedro"]["parameters"]
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
):
    """For nested access, separate `param_name` with `.`"""
    logger.info(f"Loading parameters: `{param_name}`")
    params = st.session_state["kedro"]["parameters"]
    param_path = param_name.split(".")
    set_nested_params(params, param_path, value)
