"""Create credentials file from st.secrets if credentials file is not present. Used for streamlit-cloud deployment."""

import os

import streamlit as st
import yaml
from streamlit.runtime.secrets import AttrDict


def pure_dict(dict_object):
    if type(dict_object) is not AttrDict:
        return dict_object
    else:
        return {key: pure_dict(dict_object[key]) for key in dict_object}


def create_credentials_file(overwrite: bool = False):
    if overwrite is True or not os.path.exists("conf/local/credentials.yml"):
        with open("conf/local/credentials.yml", "w") as f:
            yaml.dump(pure_dict(st.secrets["credentials"]), f)
