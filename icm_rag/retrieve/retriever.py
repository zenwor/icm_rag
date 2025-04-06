from typing import List, Union

import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity


class Retriever:
    def __init__(self, chunker, emb_model):
        self.chunker = chunker
        self.emb_model = emb_model

    def chunk(self, text: str):
        return self.chunker.split_text(text)

    def embed(
        self, chunks: Union[str, List[str]], batch_size: int = 1
    ) -> torch.Tensor:  # noqa: E501
        embs = (
            self.emb_model.encode(
                chunks, batch_size=batch_size, convert_to_tensor=True
            )  # noqa: E501
            .detach()
            .cpu()
        )

        return embs

    def add_chunks(self, chunks: Union[str, List[str]]):
        self.chunks = chunks
        self.embs = self.embed(chunks)

    def query(self, query: str, k: int = 10):
        # Embed the query and get the scores for all the chunks
        query_emb = self.embed(query)
        # print("query emb shape", query_emb.shape)
        # print("chunk embs shape", self.embs.shape)

        scores = cosine_similarity(query_emb.reshape(1, -1), self.embs)

        # Retrieve Top-K chunks
        top_k_idx = np.argsort(scores[0])[::-1][:k]
        top_k_chunks = [self.chunks[idx] for idx in top_k_idx]

        return top_k_chunks
