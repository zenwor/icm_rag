#!/bin/bash

# This script will set up the Conda environment and install the dependencies

CONDA_ENV_NAME="icm_rag_env"
PYTHON_VERSION="3.11"

# Check if the conda environment exists
if conda env list | grep -q "$CONDA_ENV_NAME"; then
    echo "Activating conda environment: $CONDA_ENV_NAME"
else
    echo "Conda environment '$CONDA_ENV_NAME' not found. Creating it..."
    conda create --name "$CONDA_ENV_NAME" -c conda-forge python=$PYTHON_VERSION
fi
conda activate "$CONDA_ENV_NAME"

# Install dependencies
if [[ -f "requirements.txt" ]]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping installation."
fi

# General environment variables
export PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export DOTENV_PATH="$PROJECT_ROOT/.env.example"