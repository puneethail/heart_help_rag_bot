from google import genai
from google.genai import types 
from chromadb import PersistentClient
import os
from typing import List, Tuple, Dict, Any, Union
from chromadb.utils.embedding_functions import EmbeddingFunction
from src.constants import GOOGLE_API_KEY, EMBEDDING_MODEL
client = genai.Client()
# import ufid

class GeminiEmbedder(EmbeddingFunction):
    def __init__(self, api_key : str = GOOGLE_API_KEY, model_id:str = EMBEDDING_MODEL):
        self.model_id = model_id
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)

    def __call__(self, input: List) -> List[List[float]]:
        try:
            if isinstance(input, str):
                input = [input]

            # Convert documents or other objects to plain text
            plain_texts = []
            for item in input:
                if hasattr(item, "page_content"):  # handle LangChain-style Document
                    plain_texts.append(item.page_content)
                else:
                    plain_texts.append(str(item))

               

            response = self.client.models.embed_content(
                model= self.model_id,
                contents= plain_texts,
                config=types.EmbedContentConfig(
                task_type="retrieval_document",
                title="Embedding generation"
            ))

            # Return embeddings as list of float lists
            if hasattr(response, "embeddings"):
                return [item.values for item in response.embeddings]

            # Handle unexpected response format
            raise ValueError("Unexpected response format from Gemini embedding API.")

        except Exception as ex:
            print("An exxception occered", ex)

class VectorDBManager:
    """Manages creation, storage, and retrieval of embeddings using Chroma."""

    def __init__(self, db_path: str, collection_name: str,google_api_key: str = GOOGLE_API_KEY, embedding_model_id:str =EMBEDDING_MODEL ):
        os.makedirs(db_path, exist_ok=True)
        self.db_path = db_path
        self.api_key = google_api_key
        self.collection_name = collection_name
        self.embedding_client = genai.Client(api_key=self.api_key)
        self.embedding_fn = self.embedding_client.models.embed_content(
                model= embedding_model_id,
                config=types.EmbedContentConfig(
                task_type="retrieval_document",
                title="Embedding generation"
            )
        )
        self.client = PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn
        )
    
    def store_documents(self, text: Union[str, List[str]], store: bool = True) -> List[str]:
        """Chunk text and optionally store embeddings in Chroma."""
        
        
        if store:
            ids = [f"doc_{i}" for i in range(len(text))]
            self.collection.add(documents=text, 
                                ids=ids)
            print(f"✅ Stored {len(text)} chunks in vector DB '{self.collection_name}'")
        else:
            print("⚠️ store=False → Embeddings not stored in DB.")
        
        

    def query(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Perform cosine similarity search."""
        results = self.collection.query(query_texts=[query], 
                                        n_results=top_k)
        print("\n🔍 Top Retrieved Chunks:")
        for i, doc in enumerate(results["documents"][0]):
            print(f"\nRank {i+1}:")
            print(doc[:500] + "..." if len(doc) > 500 else doc)
        return results


    

# print(result.embeddings)