#!/bin/bash

clear -x
cd $SRC_ROOT
./main.py \
    --exp_name "exp_6" \
    --dataset "wikitexts" \
    --cache_dir "$SRC_ROOT/data/cache" \
    --chunk_size 800 \
    --chunk_overlap 400 \
    --ret_type "chromadb" \
    --emb_model sentence-transformers/all-MiniLM-L6-v2 \
    --k 5 \
    --log "$EXPERIMENTS_DIR/wikitexts/experiments.csv" \
