#!/usr/bin/env python3

import os
from pathlib import Path

from dotenv import load_dotenv
from eval import Evaluation
from retrieve import FixedTokenChunker, Retriever
from sentence_transformers import SentenceTransformer
from utils import log_info  # noqa: F401
from utils import parse_args  # noqa: E501
from utils import (
    download,
    load_df,
    make_path,
    parse_txt,
    preprocess_df,
    set_log_file,
)

load_dotenv(os.getenv("DOTENV_PATH"))


if __name__ == "__main__":
    args = parse_args()

    set_log_file(args.log)

    # Download and prepare dataset
    args.dataset_dir = make_path(args.dataset_dir)
    file_path = download(
        base_url=os.getenv("DEFAULT__CORPORA_GITHUB_RAW_URL", ""),
        local_dir=args.dataset_dir,
        dataset=args.dataset,
        force_download=False,
    )
    content = parse_txt(file_path)

    questions_df = load_df(args.questions_df_path)
    questions_df = preprocess_df(questions_df, dataset=args.dataset)
    questions_df_filepath = Path(args.dataset_dir) / Path("questions_df.csv")
    questions_df.to_csv(questions_df_filepath, index=False)

    chunker = FixedTokenChunker(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
    emb_model = SentenceTransformer(args.emb_model)

    ret = Retriever(chunker, emb_model)
    ret.from_document(content)

    eval = Evaluation(ret, questions_df)
    res = eval(["recall", "precision"])

    print(f"Recall: {res['recall'] * 100:.2f}")
    print(f"Precision: {res['precision'] * 100:.2f}")
