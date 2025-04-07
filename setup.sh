#!/bin/bash

# This script will set up the Conda environment and install the dependencies

export PROJECT_NAME="icm_rag"
CONDA_ENV_NAME="${PROJECT_NAME}_env"
PYTHON_VERSION="3.11"

# Check if the conda environment exists
if conda env list | grep -q "$CONDA_ENV_NAME"; then
    echo "Conda environment '$CONDA_ENV_NAME' already exists. Updating it..."
    conda env update --name "$CONDA_ENV_NAME" --file environment.yml --prune
else
    echo "Conda environment '$CONDA_ENV_NAME' not found. Creating it from environment.yml..."
    conda env create --name "$CONDA_ENV_NAME" --file environment.yml
fi

# Activate the environment
conda activate "$CONDA_ENV_NAME"

# General environment variables
export PROJECT_ROOT=$PWD
export SRC_ROOT="${PROJECT_ROOT}/${PROJECT_NAME}/"
export DOTENV_PATH="${PROJECT_ROOT}/.env.example"
export EXPERIMENTS_DIR="${SRC_ROOT}/experiments/"
export UTILS_DIR="${SRC_ROOT}/utils/"
export DOCS_DIR="${PROJECT_ROOT}/docs/"


export PYTHONPATH=$SRC_ROOT
