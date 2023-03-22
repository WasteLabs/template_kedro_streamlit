import os
import shutil

import streamlit as st  # noqa: I201

from dashboards.kedro_wrapper import catalog, context, params
from dashboards.kedro_wrapper.pipelines import initiate_pipeline

st.set_page_config(layout="wide")

st.write("Page for testing kedro pipeline")

st.subheader("Init context")

context.start_kedro_session()
st.write("Special parameters for our `test` pipeline")
st.write(params.load("head_size"))
st.write(params.load("session_key"))

st.subheader("Init pipeline")

test_pipeline = initiate_pipeline("test")
st.write(test_pipeline)
st.write(st.session_state["kedro"]["pipelines"]["test"])

st.write("List of available parameter files")
st.write(test_pipeline.list_param_files())
st.write("Current params")
st.write(test_pipeline.params())
parameter_file = "super_test"
test_pipeline.set_key(parameter_file)
test_pipeline.set_param("session_key", parameter_file)
st.write(test_pipeline.get_param("session_key"))
test_pipeline.save_params("super_test", reload_catalog=True)
st.write(test_pipeline.list_param_files())
st.write(catalog.load("parameters__test", key=parameter_file)["session_key"])

st.subheader("Run pipeline")

st.write("Available pipeline output")
st.write(catalog.list_partition("example_iris_data_head_partitioned"))
parameter_file = "test_run"
test_pipeline.set_key(parameter_file)
test_pipeline.set_param("session_key", parameter_file)
test_pipeline.run()

st.write("List of available parameter files, new one autosaved")
st.write(test_pipeline.list_param_files())

st.write("Available pipeline output")
st.write(catalog.list_partition("example_iris_data_head_partitioned"))

st.write("Output")
st.write(catalog.load("example_iris_data_head_partitioned", key=parameter_file))


st.subheader("Run pipeline again")
parameter_file = "test_run_head_1"
test_pipeline.set_key(parameter_file)
test_pipeline.set_param("session_key", parameter_file)
test_pipeline.set_param("head_size", 1)
st.write("Available parameter files")
st.write(test_pipeline.list_param_files())
test_pipeline.run()
st.write("Available parameter files (new auto saved)")
st.write(test_pipeline.list_param_files())
st.write("Available pipeline output")
st.write(catalog.list_partition("example_iris_data_head_partitioned"))
st.write("Output")
st.write(catalog.load("example_iris_data_head_partitioned", key=parameter_file))

project_path = context.get_project_dir()

test_path = project_path + "/data/00_parameters/"
shutil.rmtree(test_path)

test_path = project_path + "/data/02_intermediate/example_iris_data_head_partitioned/"
shutil.rmtree(test_path)

test_path = project_path + "/data/02_intermediate/iris_head.csv"
os.remove(test_path)
