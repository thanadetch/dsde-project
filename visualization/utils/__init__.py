import pandas as pd

def explode_semi_colon_separated_series(keyword_series):
    keyword_series = keyword_series[keyword_series.apply(lambda x: isinstance(x, str))]
    return (item.strip() for s in keyword_series for item in s.split(";"))

def get_df_from_csv(file_path):
    return pd.read_csv(file_path, on_bad_lines="skip", engine="python")
