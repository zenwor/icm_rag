#!/bin/bash

clear -x
cd $SRC_ROOT
./main.py \
    --dataset "wikitexts" \
    --cache_dir "$SRC_ROOT/data/cache" \
    --chunk_size 800 \
    --chunk_overlap 400 \
    --emb_model sentence-transformers/all-MiniLM-L6-v2 \
    --k 10 \
