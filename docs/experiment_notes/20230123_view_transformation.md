# 🤔 Documentation of finidings

## ❓Problem statement

The solution is needed to separate view & actual data. view is derived of transformation steps

## 🏗️ Solutions

- Setup transformed pydantic.BaseModel class that organizes computations (Done under 01_view page)
    - Considered as a best because keeps together transformations & their arguments and helps to validate inputs using pydantic constructions.
- Setup sequence of `pd.DataFrame.pipe()` functions
    - Given constructions looks ugly in code
- Setup separate transformation functions
    - A lot of imports and function calls intedmediary
