# 📝 Template Kedro streamlit

Template project for integration of streamlit and kedro

## ⬛Environment management

- To create & install dependencies: `make env_configure`
- To activate python env in shell: `make env_use`

Use `source $(poetry env info --path)/bin/activate` if you are having issues.

Optional:

- To install jupyter extensions: `make env_install_jupyter_extensions`
- To install pre-commit hooks: `make env_install_precommit_hooks` (NOTE: Must be done only after activation of virtual env shell)

## 🏃 How to run streamlit application locally

- Create environment as per above
- Activate shell environment: `poetry shell`
- Execute streamlit: `make run_streamlit`

## Research

- [How to manage data over different pages with edit support and isolatency between streamlit sessions](docs/experiment_notes/20230117_adil_kedro_catelog_st_session_data_link.md.md)
