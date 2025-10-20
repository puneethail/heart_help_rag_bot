import google.genai as genai
from src.constants import GOOGLE_API_KEY, MODEL
# from src.constants.prompt import heart_prompt



# 2️⃣ Define the function
class llm:
    def __init__(self, Model: str = MODEL):
        self.model = Model
        self.client = genai.Client(api_key = GOOGLE_API_KEY)

    def genrate_response(self, query: str, context):
        prompt = f"Context:\n{context}\n\nQuestion: {query}"
        # prompt = heart_prompt + "\n" + prompt
        response = self.client.models.generate_content(
            model= self.model,
            contents=prompt,
        )

        return response.text
