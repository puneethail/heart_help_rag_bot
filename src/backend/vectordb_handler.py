import os
from typing import List, Union, Dict, Any, Optional
from uuid import uuid4

from openai import OpenAI
from chromadb import PersistentClient
from chromadb.api.types import EmbeddingFunction
from src.constants import GOOGLE_API_KEY, EMBEDDING_MODEL, CROMA_DB_PATH, COLLECTION_NAME


class OpenAIEmbeddingFunction(EmbeddingFunction):
    """
    Chroma-compatible embedding function using the OpenAI SDK.
    Works with:
      - Native OpenAI (text-embedding-3-small/large)
      - Any OpenAI-compatible endpoint (e.g., OpenRouter) by providing base_url and api_key
        and setting `model` to what that endpoint exposes (e.g., "google/text-embedding-004" on OpenRouter).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "text-embedding-3-small",
        batch_size: int = 128,
        base_url: Optional[str] = None,
        organization: Optional[str] = None,
        timeout: Optional[float] = None,
        default_headers: Optional[Dict[str, str]] = None,
    ):
        client_kwargs: Dict[str, Any] = {}
        if api_key:
            client_kwargs["api_key"] = api_key
        if base_url:
            client_kwargs["base_url"] = base_url
        if organization:
            client_kwargs["organization"] = organization
        if timeout:
            client_kwargs["timeout"] = timeout
        if default_headers:
            client_kwargs["default_headers"] = default_headers

        self.client = OpenAI(**client_kwargs)
        self.model = model
        self.batch_size = max(1, batch_size)

    def __call__(self, texts: List[str]) -> List[List[float]]:
        if isinstance(texts, str):
            texts = [texts]

        vectors: List[List[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            # OpenAI embeddings endpoint supports batch input as a list of strings
            resp = self.client.embeddings.create(model=self.model, input=batch)
            # Order is preserved; each item has `.embedding`
            vectors.extend([d.embedding for d in resp.data])
        return vectors


class VectorDBManagerOpenAI:
    """
    Vector DB manager using Chroma + OpenAI SDK embeddings (or OpenAI-compatible endpoints).
    Configured to use Google's embedding model via OpenRouter.
    """

    def __init__(
        self,
        db_path: str = CROMA_DB_PATH,
        collection_name: str = COLLECTION_NAME,
        api_key: str = GOOGLE_API_KEY,
        embedding_model_id: str = EMBEDDING_MODEL,
        batch_size: int = 99,
        base_url: Optional[str] = "https://generativelanguage.googleapis.com/v1beta/openai/",
        organization: Optional[str] = None,
        default_headers: Optional[Dict[str, str]] = None,
    ):
        os.makedirs(db_path, exist_ok=True)
        self.db_path = db_path
        self.collection_name = collection_name

        self.embedding_fn = OpenAIEmbeddingFunction(
            api_key=api_key,
            model=embedding_model_id,
            batch_size=batch_size,
            base_url=base_url,
            organization=organization,
            default_headers=default_headers,
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
        docs = [text] if isinstance(text, str) else list(text)
        if ids is None:
            ids = [str(uuid4()) for _ in docs]
        if metadatas is not None and len(metadatas) != len(docs):
            raise ValueError("metadatas length must match documents length")

        self.collection.add(documents=docs, ids=ids, metadatas=metadatas)
        print(f"✅ Stored {len(docs)} document(s) in vector DB '{self.collection_name}'")
        return ids

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        """Generate embeddings for the given text(s)."""
        docs = [text] if isinstance(text, str) else list(text)
        return self.embedding_fn(docs)

    def query(self, query: str, top_k: int = 3, printresults: bool = False) -> Dict[str, Any]:
        """Query the vector database and return top_k most similar documents."""
        results = self.collection.query(query_texts=[query], n_results=top_k)
        if printresults:
            print("\n🔍 Top Retrieved Chunks:")
            for i, doc in enumerate(results.get("documents", [[]])[0]):
                print(f"\nRank {i+1}:")
                print(doc[:500] + "..." if len(doc) > 500 else doc)
        return results

    def delete_documents(self, ids: List[str]) -> None:
        """Delete documents by their IDs."""
        self.collection.delete(ids=ids)
        print(f"🗑️ Deleted {len(ids)} document(s) from vector DB")

    def update_documents(
        self,
        ids: List[str],
        documents: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Update existing documents."""
        self.collection.update(ids=ids, documents=documents, metadatas=metadatas)
        print(f"📝 Updated {len(ids)} document(s) in vector DB")

    def get_collection_count(self) -> int:
        """Get the total number of documents in the collection."""
        return self.collection.count()

    def peek(self, limit: int = 10) -> Dict[str, Any]:
        """Peek at the first few items in the collection."""
        return self.collection.peek(limit=limit)

