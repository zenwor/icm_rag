import argparse
import os
from pathlib import Path
from typing import Union

from utils.log import log_done, log_ongoing


def parse_txt(file_path: Union[Path, str]) -> str:
    """
    Read the textual content of a file.
    Aimed to be used for document content parsing (.md format).

    Args:
        file_path (Union[Path, str]): Path to txt-parsable file.

    Returns:
        content (str): Parsed textual content, in UTF-8 encoding.
    """
    log_ongoing(f"Reading the content of file: {file_path}...")
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    log_done("Successfully loaded file contents.")
    return content


def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--exp_name",
        type=str,
        default="default_experiment",
        help="Name of the experiment run with the given parameters.",
    )

    parser.add_argument(
        "--questions_df_path",
        type=str,
        help="Path to questions DataFrame.",
        default=os.getenv("DEFAULT__QUESTIONS_DF_PATH"),
    )
    parser.add_argument(
        "--dataset",
        type=str,
        choices=["chatlogs", "state_of_the_union", "wikitexts"],
        required=True,
    )
    parser.add_argument(
        "--cache_dir",
        type=str,
        help="Path to caching directory.",
        default=os.getenv("DEFAULT__CACHE_DIR"),
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        help="Path to data directory.",
        default=os.getenv("DEFAULT__DATA_DIR"),
    )
    parser.add_argument(
        "--dataset_dir",
        type=str,
        help="Path to store downloaded dataset.",
        default=os.getenv("DEFAULT_DATASET_DIR"),
    )
    parser.add_argument(
        "--log",
        type=str,
        help="Path to log file.",
        default=None,
    )

    parser.add_argument(
        "--ret_type",
        type=str,
        choices=["cos_sim", "chromadb"],
        help="Type of vector database to use.",
        default="chromadb",
    )
    parser.add_argument(
        "--chunk_size",
        type=int,
        default=400,
        help="Chunk size to use for document chunking.",
    )
    parser.add_argument(
        "--chunk_overlap",
        type=int,
        default=40,
        help="Chunk overlap to use for document chunking.",
    )
    parser.add_argument(
        "--emb_model",
        type=str,
        default="sentence-transformers/all-MiniLM-L6-v2",
        choices=[
            "sentence-transformers/all-MiniLM-L6-v2",
            "sentence-transformers/multi-qa-mpnet-base-dot-v1",
        ],
        help="Chunk embedding model.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=16,
        help="Batch size for chunk embedding.",
    )
    parser.add_argument(
        "--k", type=int, default=10, help="Retrieve top-k chunks."
    )  # noqa: E501

    return parser.parse_args()
