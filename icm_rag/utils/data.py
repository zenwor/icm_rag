import pandas as pd


def load_df(df_path: str) -> pd.DataFrame:
    return pd.read_csv(df_path)


def preprocess_df(df: pd.DataFrame, dataset: str) -> pd.DataFrame:
    df = df[df["corpus_id"] == dataset]

    return df
