#!/bin/bash

clear -x
cd $SRC_ROOT
./main.py \
    --exp_name "exp_11" \
    --dataset "chatlogs" \
    --cache_dir "$SRC_ROOT/data/cache" \
    --chunk_size 800 \
    --chunk_overlap 400 \
    --ret_type "cos_sim" \
    --emb_model sentence-transformers/all-MiniLM-L6-v2 \
    --k 10 \
    --log "$EXPERIMENTS_DIR/chatlogs/experiments.csv" \
