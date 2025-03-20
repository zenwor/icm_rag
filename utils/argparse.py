from utils.path import make_path

import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--questions_df_path", 
        type=str,
        help="Path to questions DataFrame.",
        default=os.getenv("DEFAULT__QUESTIONS_DF_PATH"),
    )
    parser.add_argument(
        "--dataset", 
        type=str,
        choices=["chatlogs", "state_of_the_union", "wikitext"],
        required=True,
    )
    parser.add_argument(
        "--cache_dir", 
        type=str,
        help="Path to caching directory.",
        default=os.getenv("DEFAULT__CACHE_DIR")
    )
    parser.add_argument(
        "--data_dir", 
        type=str,
        help="Path to data directory.",
        default=os.getenv("DEFAULT__DATA_DIR")
    )
    parser.add_argument(
        "--dataset_dir", 
        type=str,
        help="Path to store downloaded dataset.",
        default=os.getenv("DEFAULT_DATASET_DIR")
    )
    parser.add_argument(
        "--log", 
        type=str,
        help="Path to log file.",
        default=None,
    )
    
    return parser.parse_args()