#!/usr/bin/env python3

import os
from pathlib import Path

from dotenv import load_dotenv
from utils import parse_args  # noqa: E501
from utils import download, load_df, make_path, preprocess_df, set_log_file

load_dotenv(os.getenv("DOTENV_PATH"))


if __name__ == "__main__":
    args = parse_args()

    set_log_file(args.log)

    # Download and prepare dataset
    args.dataset_dir = make_path(args.dataset_dir)
    download(
        base_url=os.getenv("DEFAULT__CORPORA_GITHUB_RAW_URL", ""),
        local_dir=args.dataset_dir,
        dataset=args.dataset,
    )

    questions_df = load_df(args.questions_df_path)
    questions_df = preprocess_df(questions_df, dataset=args.dataset)
    questions_df_filepath = Path(args.dataset_dir) / Path("questions_df.csv")
    questions_df.to_csv(questions_df_filepath, index=False)
