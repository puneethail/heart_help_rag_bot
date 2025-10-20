import gradio as gr
import random
# for LLM Response (RAG Funtinality)
from src.backend.llm import llm


def chat_response(message, history):
    # calling llm
    responses = llm_obj.llm_with_history(query=message)
    
    return responses

if __name__ == "__main__":
    # Creating LLM object 
    llm_obj = llm()
    demo = gr.ChatInterface(
        fn=chat_response,
        # 'messages' format for history: list of dicts with 'role' and 'content' (like OpenAI API)
        type="messages", 
        title="Heart help app"
    )
    
    # Launch the app
    demo.launch()