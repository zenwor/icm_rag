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

    @staticmethod
    def from_kwargs(**kwargs):
        """
        Create an instance of child-class Retriever, based on provided `type`.
        Current options include:
            "cos_sim": CosSimRetriever (custom, simple implementation)
            "chromadb": ChromaDBRetriever (implemented using `chromadb` module).

        Args:
            **kwargs: Keyword arguments
                type (str): Type of retriever to initialize and return.
                chunker: Chunker to pass for retriever.
                emb_model: Embedding model.

        Returns:
            Retriever: Initialized retriever of type `type`, with `chunker`
                and `emb_model` set. No chunks are added in this part of
                pipeline.
        """

        TYPE_TO_CLASS = {
            "cos_sim": CosSimRetriever,
            "chromadb": ChromaDBRetriever,
        }
        type = kwargs["type"]
        if type not in TYPE_TO_CLASS:
            raise ValueError(f"Invalid retriever type selected: {type}")

        type_class = TYPE_TO_CLASS[type]
        return type_class(kwargs["chunker"], kwargs["emb_model"])

    def chunk(self, text: str) -> List[str]:
        """
        Chunk given text.

        Args:
            text (str): Text to chunk using the chunker provided.
                Chunker, upon initialization, has set `chunk_size` and
                `chunk_overlap`.

        Returns:
            List[str]: List of chunks.
        """
        return []

    def embed(self, chunks: Union[str, List[str]], batch_size: int = 1) -> torch.Tensor:
        """
        Embed a single chunk, or a list of chunks.
        This method is also used for query embedding.

        Args:
            chunks (Union[str, List[str]]): Chunk(s), i.e. the textual content,
                to embed using embedding model.
            batch_size (int): Size of a single batch to load into the memory.

        Returns:
            torch.Tensor: Embedding of given chunk(s).
                If multiple chunks, will return the embedding in the shape of
                (num_chunks, embedding_size).
        """
        return None

    def query(self, query: str, k: int = 10) -> List[dict]:
        """
        Query retriever for top-k relevant chunks.

        Args:
            query (str): Textual representation of query.
            k (int): Maximum number of chunks to retrieve.

        Returns:
            List[dict]: List of retrieved chunks, complete with textual content,
                embeddings and metadata.
        """
        return []

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
        """
        Generate metadata pieces for given chunk.
        As of now, method only finds the start and index of each chunk, inside
        given document.

        Args:
            chunk (str): Chunk to generate metadata for.
            document (str): Original, full document, chunk was created from.

        Returns:
            dict: Metadata pieces for given chunk.
        """
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


class ChromaDBRetriever(Retriever):
    """
    This class contains implementation of standard ChromaDB, as vector store,
    for retrieval purposes.
    """


class CosSimRetriever(Retriever):
    """
    This class contains simple implementation of cosine similarity retriever.
    As the name suggests, will use cosine_similarity to calculate similarities
    between query embedding and each chunk embedding.
    """

    def __init__(self, chunker, emb_model):
        super().__init__(chunker, emb_model)

    def __getitem__(self, idx: int):
        """
        Implemented as part of easier access.
        Returns the chunk at given index, with all accompanying embeddings
        and metadata.

        Args:
            idx (int): Index of the chunk.

        Returns:
            dict: Dictionary containing:
                (1) "chunk" (str): Textual content of the chunk
                (2) "emb" (torch.Tensor): Chunk embedding.
                (3) "metadata" (dict): Dictionary of chunk metadata.
                    As of now, only contains `start_index` and `end_index`.
        """
        # In case of invalid chunk number, return None
        if idx >= len(self.chunks):
            return None

        # Return full chunk information
        return {
            "chunk": self.chunks[idx],
            "emb": self.embs[idx],
            "metadata": self.metadata[idx],
        }

    def __iter__(self):
        """
        Iterate over all chunks and yield each chunk with all accompanying data.
        """
        for idx in range(len(self.chunks)):
            yield self.__getitem__(idx)

    def chunk(self, text: str) -> List[str]:
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

    def add_chunks(
        self, chunks: Union[str, List[str]], metadata: List[dict] = []
    ) -> None:
        self.chunks = chunks
        self.embs = self.embed(chunks)
        self.metadata = metadata

    def from_document(self, content: str, add_metadata: bool = True) -> None:
        """
        Create chunk database from given document (content).
        Split document into chunks, embed the chunks, and, if applicable,
        generate metadata pieces for each chunk.

        Args:
            content (str): Document to chunk.
            add_metadata (bool): If true, will generate metadata for each chunk.
                Otherwise, metadata is `None` for all chunks.

        Returns:
            None
        """
        chunks = self.chunk(content)

        metadata = None
        if add_metadata:
            metadata = []
            for chunk in chunks:
                chunk_metadata = super()._make_metadata_for_chunk(chunk, content)
                metadata.append(chunk_metadata)

        self.add_chunks(chunks, metadata=metadata)

    def query(self, query: str, k: int = 10):
        # Embed the query and get the scores for all the chunks
        query_emb = self.embed(query)
        scores = cosine_similarity(query_emb.reshape(1, -1), self.embs)

        # Retrieve Top-K chunks, with full embeddings and metadat
        top_k_idx = np.argsort(scores[0])[::-1][:k]
        full_chunks = [self.__getitem__(idx) for idx in top_k_idx]

        return full_chunks
