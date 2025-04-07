import pandas as pd
from utils.log import log_done, log_ongoing


def load_df(df_path: str) -> pd.DataFrame:
    """
    Load DataFrame. Aimed to be used for questions DataFrame.

    Args:
        df_path (str): Path to the DataFrame. Can be URL.

    Returns:
        pd.DataFrame: Downloaded CSV file, wrapped into DataFrame object.
    """
    log_ongoing(f"Loading CSV at: {df_path}")
    df = pd.read_csv(df_path)
    log_done(f"Successfully loaded DataFrame!")

    return df


def preprocess_df(df: pd.DataFrame, dataset: str) -> pd.DataFrame:
    """
    Preprocess DataFrame. Aimed to be used for questions DataFrame.
    Transformations:
        (1) Filtering by dataset name - include only columns of value `dataset`.

    Args:
        df (pd.DataFrame): DataFrame to preprocess.
        dataset (str): Dataset used for reference.

    Returns:
        df (pd.DataFrame): Preprocessed DataFrame.
    """
    log_ongoing(f"Preprocessing DataFrame...")
    df = df[df["corpus_id"] == dataset]
    log_done(f"Successfully preprocessed DataFrame!")

    return df
