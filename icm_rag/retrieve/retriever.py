import re
from typing import Dict, List, Union

import numpy as np
import torch
from fuzzywuzzy import fuzz, process
from sklearn.metrics.pairwise import cosine_similarity


class Retriever:
    def __init__(self, chunker, emb_model):
        self.chunker = chunker
        self.emb_model = emb_model

    def __getitem__(self, idx: int):
        if idx >= len(self.chunks):
            return None

        return {
            "chunk": self.chunks[idx],
            "emb": self.embs[idx],
            "metadata": self.metadata[idx],
        }

    def __iter__(self):
        for idx in range(len(self.chunks)):
            yield self.__getitem__(idx)

    def chunk(self, text: str):
        return self.chunker.split_text(text)

    def embed(
        self, chunks: Union[str, List[str]], batch_size: int = 1
    ) -> torch.Tensor:  # noqa: E501
        embs = (
            self.emb_model.encode(
                chunks,
                batch_size=batch_size,
                convert_to_tensor=True,
                show_progress_bar=False,
            )  # noqa: E501
            .detach()
            .cpu()
        )

        return embs

    def add_chunks(self, chunks: Union[str, List[str]], metadata: List[dict] = []):
        self.chunks = chunks
        self.embs = self.embed(chunks)
        self.metadata = metadata

    # Taken from author's implementation
    def _find_query_despite_whitespace(self, chunk: str, document: str):
        # Normalize spaces and newlines in the query
        normalized_query = re.sub(r"\s+", " ", chunk).strip()

        # Create a regex pattern from the normalized chunk
        # to match any whitespace characters between words
        pattern = r"\s*".join(
            re.escape(word) for word in normalized_query.split()
        )  # noqa: E203

        # Compile the regex to ignore case and search for it in the document
        regex = re.compile(pattern, re.IGNORECASE)
        match = regex.search(document)

        if match:
            return (
                document[match.start() : match.end()],  # noqa: E203
                match.start(),
                match.end(),
            )  # noqa: E203
        else:
            return None

    # Taken from author's implementation
    def _rigorous_document_search(self, chunk: str, document: str):
        if chunk.endswith("."):
            chunk = chunk[:-1]

        if chunk in document:
            start_index = document.find(chunk)
            end_index = start_index + len(chunk)
            return chunk, start_index, end_index
        else:
            raw_search = self._find_query_despite_whitespace(chunk, document)
            if raw_search is not None:
                return raw_search

        # Split the text into sentences
        sentences = re.split(r"[.!?]\s*|\n", document)

        # Find the sentence that matches the query best
        best_match = process.extractOne(
            chunk, sentences, scorer=fuzz.token_sort_ratio
        )  # E501

        if best_match[1] < 98:
            return None

        reference = best_match[0]

        start_index = document.find(reference)
        end_index = start_index + len(reference)

        return reference, start_index, end_index

    def _make_metadata_for_chunk(self, chunk: str, document: str) -> Dict:
        # Get starting and ending position of chunk within the document
        try:
            _, start_index, end_index = self._rigorous_document_search(
                chunk,
                document,
            )
        except Exception:
            start_index = -1
            end_index = -1

        return {
            "start_index": start_index,
            "end_index": end_index,
        }

    def from_document(self, content: str, add_metadata: bool = True):
        chunks = self.chunk(content)

        metadata = None
        if add_metadata:
            metadata = []
            for chunk in chunks:
                chunk_metadata = self._make_metadata_for_chunk(chunk, content)
                metadata.append(chunk_metadata)

        self.add_chunks(chunks, metadata=metadata)

    def query(self, query: str, k: int = 10):
        # Embed the query and get the scores for all the chunks
        query_emb = self.embed(query)
        # print("query emb shape", query_emb.shape)
        # print("chunk embs shape", self.embs.shape)

        scores = cosine_similarity(query_emb.reshape(1, -1), self.embs)

        # Retrieve Top-K chunks, with full embeddings and metadat
        top_k_idx = np.argsort(scores[0])[::-1][:k]
        full_chunks = [self.__getitem__(idx) for idx in top_k_idx]

        return full_chunks
