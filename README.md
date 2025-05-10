# 🤖Intelligent chunking methods for code documentation RAG

**ICM_RAG** is experimentation with retrieval pipeline, for general textual corpora retrieval task.

## 🏗 Implementation
### ℹ️ General
**ICM_RAG** aims to implement a retrieval pipeline, with an already defined chunker ([FixedTokenChunker](https://github.com/brandonstarxel/chunking_evaluation/blob/main/chunking_evaluation/chunking/fixed_token_chunker.py)), and a dataset of choice: Wikitexts, Chatlogs and State of the Union. All the datasets can be found [here](https://github.com/brandonstarxel/chunking_evaluation/tree/main/chunking_evaluation/evaluation_framework/general_evaluation_data/corpora). One may choose the model, but for the specifics of the task, `sentence-transformers/all-MiniLM-L6-v2` was chosen. It is intuitve to set it to some other model, say `sentence-transformers/multi-qa-mpnet-base-dot-v1`, by tweaking the cmdline arguments.

### 💻 Command-line arguments

| Argument Name                           | Description | Value Range   | Default Value |
|-----------------------------------------|-------------|---------------|---------------|
| exp_name                                | Experiment name. | `str` | `default_experiment` |
| questions_df_path | Path to questions DataFrame |  | (.env) `DEFAULT__QUESTIONS_DF_PATH` |
| dataset | Name of the dataset to use. |  `wikitexts`, `chatlogs`, `state_of_the_union` | (.env) `DEFAULT__QUESTIONS_DF_PATH` |
| cache_dir | Path to caching directory. | | (.env) `DEFAULT_CACHE_DIR` |
| data_dir | Path to data directory. | | (.env) `DEFAULT__DATA_DIR` |
| dataset_dir | Path to dataset directory. | | (.env) `DEFAULT_DATASET_DIR` |
| log | Path to (experiment) log file. | | None |
| ret_type | Type of retriever to use. | `cos_sim`, `chromadb` | `chromadb` |
| chunk_size | Chunk size to use for document chunking | `int` | 400 |
| chunk_overlap | Chunk overlap to use for document chunking. | `int` | 40 |
| emb_model | Embedding model. | `sentence-transformers/all-MiniLM-L6-v2`, `sentence-transformers/multi-qa-mpnet-base-dot-v1`, | `sentence-transformers/all-MiniLM-L6-v2` |
| batch_size | Batch size for model embedding. | int | 16 |
| k | Retrieve top-k chunks | `int` | 10 |

## 🚀 Quickstart
**ICM_RAG** uses `conda` for environment management. To clone the repository and set up the environment, i.e. create it and install the dependencies, you may run:
```bash
git clone https://github.com/LukaNedimovic/icm_rag.git
cd icm_rag
source ./setup.sh
```
`setup.sh` will also export several environment variables, useful for dynamic path creation and, therefore, setting up the configurations for experiments.

## 🧪 Experiments
**ICM_RAG** comes with a set of 30 experiments (10 for each dataset).

The main goal was to check for the effects of chunk size / overlap, and top-K retrieved chunks. You may find experiment results here: [Experiment Results Paper](./icm_rag/experiments/ICM_RAG%20-%20Experiment%20Results.pdf).

You may find experiment examples in the [experiments directory](./icm_rag/experiments/), however, here is another quick example:
```bash
./main.py \
    --exp_name "example_experiment" \
    --dataset "wikitexts" \
    --emb_model "sentence-transformers/multi-qa-mpnet-base-dot-v1" \
    --cache_dir "$SRC_ROOT/data/cache" \
    --chunk_size 1500 \
    --chunk_overlap 500 \
    --ret_type "chromadb" \
    --log "$EXPERIMENTS_DIR/wikitexts/experiments.csv" \
    --k 12
```

## 📝 Documentation
To build the documentation, it is enough to run the `setup.sh` and the `build_docs.sh`:
```bash
source ./setup.sh
./build_docs.sh
```
By default, the `build_docs.sh` will open the `docs/build/index.html` using Firefox.
