import os

import streamlit as st  # noqa: I201

from dashboards.kedro_wrapper import catalog, context, params

st.set_page_config(layout="wide")

st.write("Page for testing kedro wrapper")

st.subheader("Init context")

context.start_kedro_session()
st.success(st.session_state["kedro"])

st.subheader("Test parameters loaded")

test_path = "dashboards.pages.main.text"
st.write("Test path: ", test_path)
st.success(params.load(test_path))

test_path = "dashboards.pages.main"
st.write("Test path: ", test_path)
st.success(params.load(test_path))

test_path = "dashboards"
st.write("Test path: ", test_path)
st.success(params.load(test_path))

st.subheader("Test parameters saved")

test_path = "dashboards.pages.main.text"
value = "New_value"
st.write("Test path: ", test_path, value)
params.save(test_path, value)
st.success(params.load(test_path))

test_path = "dashboards.pages.main"
value = {"test1", "test2"}
st.write("Test path: ", test_path, value)
params.save(test_path, value)
st.success(params.load(test_path))

test_path = "dashboards.pages"
value = ["1", "2", "3"]
st.write("Test path: ", test_path, value)
params.save(test_path, value)
st.success(params.load(test_path))

st.subheader("Test parameters re-loaded")

context.reload_parameters()

test_path = "dashboards.pages.main.text"
st.write("Test path: ", test_path)
st.success(params.load(test_path))

st.header("Test catalog load")

df = catalog.load("example_iris_data")
st.write(df)

st.write("Should give an error:")
try:
    catalog.load("example_iris_data_save")
except:
    st.error("Error")

st.write("Save and load (works even though it's in memory):")
catalog.save("example_iris_data_save", df.head(1))
df_head = catalog.load("example_iris_data_save")
st.write(df_head)


st.write("Save and load to file:")
catalog.save("example_iris_data_save_2", df.head(1))
df_head = catalog.load("example_iris_data_save_2")
st.write(df_head)


st.write("Check context reset")
context.reload_catalog()
st.write("Should give an error again:")
try:
    df_head = catalog.load("example_iris_data_save")
except:
    st.error("Error")

st.write("But this will work:")
df_head = catalog.load("example_iris_data_save_2")
st.write(df_head)

st.write("Cleaning up the test file:")
test_path = (
    st.session_state["kedro"]["config"]["project_dir"]
    + "/data/02_intermediate/iris_save_2.csv"
)
st.success(os.path.exists(test_path))
os.remove(test_path)
st.success(os.path.exists(test_path))