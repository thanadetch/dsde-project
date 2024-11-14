import pandas as pd
from pandas import DataFrame


def explode_semi_colon_separated_series(keyword_series):
    keyword_series = keyword_series[keyword_series.apply(lambda x: isinstance(x, str))]
    return (item.strip() for s in keyword_series for item in s.split(";"))


def get_df_from_csv(file_path):
    return pd.read_csv(file_path, on_bad_lines="skip", engine="python")


def transform_data(df: DataFrame):
    df["document_id"] = df["document_id"].astype("string")
    df["affiliation_countries"] = df["affiliation_countries"].astype("string")
    df["affiliation_cities"] = df["affiliation_cities"].astype("string")
    df["affiliation_names"] = df["affiliation_names"].astype("string")
    df["title"] = df["title"].astype("string")
    df["description"] = df["description"].astype("string")
    df["publication_date"] = pd.to_datetime(df["publication_date"], errors="coerce")
    df["keywords"] = df["keywords"].astype("string")
    df["publisher"] = df["publisher"].astype("string")
    return df
