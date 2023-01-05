# 📝 Template Kedro streamlit

Template project for integration of UI of streamlit to data pipelines

## ⬛ How to manage environment

- To create & install dependencies: `make env_configure`
- To activate python env in shell: `make env_use`
- To install jupyter extensions: `make env_install_jupyter_extensions`
- To install pre-commit hooks: `make env_install_precommit_hooks` (NOTE: Must be done only after activation of virtual env shell)

## 🏃 How to run streamlit application locally

- Before running you need to create environment following section above
- Activate shell environment: `poetry shell`
- Execute streamlit by hitting: `make run_streamlit`
