import dotenv
import os
dotenv.load_dotenv()
# print(os.getenv())
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL: str = "models/text-embedding-004"
MODEL: str = "gemini-2.5-flash"


COLLECTION_NAME = "heart_data_vb"
CROMA_DB_PATH = r"src\chroma_data"
