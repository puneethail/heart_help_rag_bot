import os
from typing import List, Union, Dict, Any, Optional
from uuid import uuid4

from google import genai  # Uses google-genai 1.45.0
from chromadb import PersistentClient
from chromadb.api.types import EmbeddingFunction
from google.genai import types
from src.constants import GOOGLE_API_KEY, EMBEDDING_MODEL

class GeminiEmbeddingFunction(EmbeddingFunction):
    """
    Chroma-compatible embedding function using google-genai (v1.45.0).
    Calls client.models.embed_content with 'contents' and a types.EmbedContentConfig.
    """

    def __init__(
        self,
        api_key: str = GOOGLE_API_KEY,
        model: str = EMBEDDING_MODEL,
        task_type: str = "retrieval_document",
        title: str = "Embedding generation",
    ):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.task_type = task_type
        self.title = title

    def __call__(self, texts: List[str]) -> List[List[float]]:
            if isinstance(texts, str):
                texts = [texts]

            embeddings: List[List[float]] = []
            for t in texts:
                resp = self.client.models.embed_content(
                    model=self.model,
                    contents=t,
                    config=types.EmbedContentConfig(
                        task_type=self.task_type,
                        title=self.title,
                    ),
                )

                # Extract embedding vector robustly
                if hasattr(resp, "embedding") and hasattr(resp.embedding, "values"):
                    embeddings.append(list(resp.embedding.values))
                elif isinstance(resp, dict):
                    emb = resp.get("embedding")
                    if isinstance(emb, dict) and "values" in emb:
                        embeddings.append(list(emb["values"]))
                    elif isinstance(emb, list):
                        embeddings.append(emb)
                    else:
                        raise RuntimeError("Unexpected response format from embed_content (dict without 'embedding').")
                else:
                    raise RuntimeError("Unexpected response format from embed_content.")
            return embeddings

class VectorDBManager:
    """Manages creation, storage, and retrieval of embeddings using Chroma."""

    def __init__(
        self,
        db_path: str,
        collection_name: str,
        google_api_key: str = GOOGLE_API_KEY,
        embedding_model_id: str = EMBEDDING_MODEL,
    ):
        os.makedirs(db_path, exist_ok=True)
        self.db_path = db_path
        self.collection_name = collection_name

        # Embedding function using google-genai client
        self.embedding_fn = GeminiEmbeddingFunction(
            api_key=google_api_key,
            model=embedding_model_id,
            task_type="retrieval_document",
            title="Embedding generation",
        )

        self.client = PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn,
        )

    def store_documents(
        self,
        text: Union[str, List[str]],
        ids: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> List[str]:
        """
        Store documents; Chroma will call the embedding function for you.
        Returns the list of IDs that were stored.
        """
        docs = [text] if isinstance(text, str) else list(text)
        if ids is None:
            ids = [str(uuid4()) for _ in docs]

        if metadatas is not None and len(metadatas) != len(docs):
            raise ValueError("metadatas length must match documents length")

        self.collection.add(documents=docs, ids=ids, metadatas=metadatas)
        print(f"✅ Stored {len(docs)} document(s) in vector DB '{self.collection_name}'")
        return ids

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        """
        Return embeddings without storing them in the DB.
        """
        docs = [text] if isinstance(text, str) else list(text)
        return self.embedding_fn(docs)

    def query(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Perform cosine similarity search."""
        results = self.collection.query(query_texts=[query], n_results=top_k)
        print("\n🔍 Top Retrieved Chunks:")
        for i, doc in enumerate(results.get("documents", [[]])[0]):
            print(f"\nRank {i+1}:")
            print(doc[:500] + "..." if len(doc) > 500 else doc)
        return results