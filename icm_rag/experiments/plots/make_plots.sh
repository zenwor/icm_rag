#!/bin/bash

# This script will generate all the necessary plots, given as a part of documentation

cd $UTILS_DIR

# Database choice vs Dataset
# FUNC=recall_vs_precision ./plot.py \
#     "ret_type" \
#     "$EXPERIMENTS_DIR/wikitexts/experiments.csv" \
#     "$EXPERIMENTS_DIR/plots/recall_vs_precision_database_wikitexts.png"

# FUNC=recall_vs_precision ./plot.py \
#     "ret_type" \
#     "$EXPERIMENTS_DIR/chatlogs/experiments.csv" \
#     "$EXPERIMENTS_DIR/plots/recall_vs_precision_database_chatlogs.png"

# FUNC=recall_vs_precision ./plot.py \
#     "ret_type" \
#     "$EXPERIMENTS_DIR/state_of_the_union/experiments.csv" \
#     "$EXPERIMENTS_DIR/plots/recall_vs_precision_database_sotu.png"

# K choice vs Dataset
FUNC=recall_vs_precision ./plot.py \
    "k" \
    "$EXPERIMENTS_DIR/wikitexts/experiments.csv" \
    "$EXPERIMENTS_DIR/plots/recall_vs_precision_k_wikitexts.png"

FUNC=recall_vs_precision ./plot.py \
    "k" \
    "$EXPERIMENTS_DIR/chatlogs/experiments.csv" \
    "$EXPERIMENTS_DIR/plots/recall_vs_precision_k_chatlogs.png"

FUNC=recall_vs_precision ./plot.py \
    "k" \
    "$EXPERIMENTS_DIR/state_of_the_union/experiments.csv" \
    "$EXPERIMENTS_DIR/plots/recall_vs_precision_k_sotu.png"

# Chunk Size and Chunk Ooverlap vs Dataset
FUNC=recall_vs_precision ./plot.py \
    "chunk_size" "chunk_overlap" \
    "$EXPERIMENTS_DIR/wikitexts/experiments.csv" \
    "$EXPERIMENTS_DIR/plots/recall_vs_precision_cs_co_wikitexts.png"

FUNC=recall_vs_precision ./plot.py \
    "chunk_size" "chunk_overlap" \
    "$EXPERIMENTS_DIR/chatlogs/experiments.csv" \
    "$EXPERIMENTS_DIR/plots/recall_vs_precision_cs_co_chatlogs.png"

FUNC=recall_vs_precision ./plot.py \
    "chunk_size" "chunk_overlap" \
    "$EXPERIMENTS_DIR/state_of_the_union/experiments.csv" \
    "$EXPERIMENTS_DIR/plots/recall_vs_precision_cs_co_sotu.png"
