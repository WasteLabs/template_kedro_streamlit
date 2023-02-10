import logging

import geopandas as gpd

import pandas as pd

from pydantic import BaseModel
from pydantic import Field


class ViewTransformer(BaseModel):
    """
    Dataclass for organization of transformation steps for pd.DataFrame and gpd.GeoDataFrame
    """
    duplicate_arg: dict[str, str] = Field(
        default={},
        description="Arguments for upsert (target <= source) operation",
    )
    rename_arg: dict[str, str] = Field(
        default={},
        description="Arguments for rename step",
    )
    soft_upsert_arg: dict[str, str] = Field(
        default={},
        description="Adds column with default value if they are missing. format: column: default_value",
    )
    fillna_arg: dict[str, str] = Field(
        default={},
        description="Adds missing values to specified arguments",
    )
    replace_arg: dict[str, dict[str, str]] = Field(
        default={},
        description="Replace values in columns (format: column: value_from: value_to)",
    )
    drop_arg: list[str] = Field(
        default={},
        description="Arguments for upsert",
    )

    def __ensure_dataframe(self, df: pd.DataFrame):
        is_dataframe = isinstance(df, pd.DataFrame) or isinstance(df, gpd.GeoDataFrame)
        assert is_dataframe, "Must be pandas.DataFrame"

    def copy(self, df: pd.DataFrame) -> pd.DataFrame:
        self.__ensure_dataframe(df)
        for target, source in self.duplicate_arg.items():
            df[target] = df[source]
        return df

    def rename(self, df: pd.DataFrame) -> pd.DataFrame:
        self.__ensure_dataframe(df)
        df = df.rename(self.rename_arg)
        return df

    def upsert(self, df: pd.DataFrame) -> pd.DataFrame:
        self.__ensure_dataframe(df)
        for column, value in self.soft_upsert_arg.items():
            if column not in df.columns:
                df[column] = value
            else:
                df[column] = df[column].fillna(value)
        return df

    def fillna(self, df: pd.DataFrame) -> pd.DataFrame:
        self.__ensure_dataframe(df)
        for column, value in self.fillna_arg.items():
            if column in df.columns:
                df[column] = df[column].fillna(value)
            else:
                logging.info(f"No such column: {column} at fillna() operation")
        return df

    def drop_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        self.__ensure_dataframe(df)
        df = df.drop(columns=self.drop_arg)
        return df

    def replace(self, df: pd.DataFrame) -> pd.DataFrame:
        self.__ensure_dataframe(df)
        for columns, values in self.replace_arg.items():
            df[columns] = df[columns].replace(values)
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.__ensure_dataframe(df)
        df = self.copy(df)
        df = self.rename(df)
        df = self.upsert(df)
        df = self.fillna(df)
        df = self.replace(df)
        df = self.drop_columns(df)
        return df
