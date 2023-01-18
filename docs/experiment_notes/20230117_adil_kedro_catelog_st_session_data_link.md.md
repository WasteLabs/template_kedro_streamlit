# 🤔 Documentation of finidings

- After opening concurrent page streamlit cleans all objects in `session_state`

## ❓Problem statement

Team need solution of setting up data communication over pages in DAG flow style. Ideally uniform interface is needed and isolation between sessions is required, for example: when you open 3 different pages, changes made on each one must not affect to each other. Additionally, session must to keep the state of edited over pages, for example: when i edit table, table must change it's state in session_state and when i open view page, those edits are must be reflected respectivelly.

## 🏗️ Experiments iterations

### Iteration 1 | store kedro.parameters & kedro.catalog in a streamlit.session_state object at application start-up

Results: Very first session of streamlit was complitely fine & worked, however over time was spotted that when concurrent pages are opened everything `kedro.catalog` and `kedro.parameters` are missing in `session_state`. Was made a conclusion that `session_state` is gets cleaned after opening a new session state.

### Iteration 2 | store kedro.parameters & kedro.catalog in a streamlit.session_state object using decorator if such are missing

Results: it worked out, during testing were't spotted any each other affections & data are succesfully kept their states between page changes
