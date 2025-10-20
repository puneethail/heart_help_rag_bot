import google.genai as genai
from src.constants import GOOGLE_API_KEY, MODEL, CROMA_DB_PATH, COLLECTION_NAME, MAX_CONVERSATION_HISTORY
from src.backend.vectordb_handler import VectorDBManagerOpenAI

from src.backend.conversation import ConversationHistory
# from src.constants.prompt import heart_prompt


# 2️⃣ Define the function
class llm:
    def __init__(self, Model: str = MODEL, vdb_path: str = CROMA_DB_PATH, collection_name:str = COLLECTION_NAME, max_history: int = MAX_CONVERSATION_HISTORY):
        self.model = Model
        self.client = genai.Client(api_key = GOOGLE_API_KEY)
        self.vdb = VectorDBManagerOpenAI(
            db_path= vdb_path,
            collection_name= collection_name
            )
        self.conversation = ConversationHistory(max_history= max_history)

    def genrate_response(self, query: str):
        context = self.vdb_query(prompt= prompt)
        prompt = f"Context:\n{context}\n\nQuestion: {query}"
        # prompt = heart_prompt + "\n" + prompt
        response = self.client.models.generate_content(
            model= self.model,
            contents=prompt,
        )

        return response.text
    def vdb_query(self, query):
        return self.vdb.query(query = query)

    def llm_with_history(self ,query:str):
        # Get formatted history
        history_context = self.conversation.get_history_string()
        context = self.vdb_query(query= query)
        # Build prompt with history
        prompt = f"""Previous Conversation:
        {history_context}

        Context (from documents):
        {context}

        Current Question: {query}

        Please answer the current question, considering the conversation history if relevant."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        # Add this exchange to history
        self.conversation.add_exchange(query, response.text)

        return response.text
