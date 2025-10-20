from src.constants import GOOGLE_API_KEY
from google import genai as genai
# Initialize conversation history
from src.backend.llm import llm
    
if __name__ == "__main__":
    llm_ob = llm()
    while True:
        user_query = input("You: ")

        if user_query.lower() in ['exit', 'quit']:
           print(f"Assistant:Thank you for the conversation! If you have any more questions in the future, feel free to ask.")
           break
        
        # Query vector DB for relevant context

        # Generate response with history
        response = llm_ob.llm_with_history(query= user_query)

        print(f"Assistant: {response}\n")