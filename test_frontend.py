import gradio as gr
import random
from src.backend.llm import llm


def chat_response(message, history):
    # 'history' is a list of lists/dictionaries containing the conversation so far.
    # The format depends on the 'type' parameter (default is 'messages').
    responses = llm_obj.llm_with_history(query=message)
    # Simple example logic: a random response
    # responses = ["Hello, how can I help you?", "That's an interesting question!", "Tell me more."]
    # bot_message = random.choice(responses)
    
    # You would replace this with your actual chatbot logic (e.g., calling an LLM API)
    
    return responses

if __name__ == "__main__":
    demo = gr.ChatInterface(
        fn=chat_response,
        # 'messages' format for history: list of dicts with 'role' and 'content' (like OpenAI API)
        type="messages", 
        title="My Simple Gradio Chatbot"
    )
    llm_obj = llm()
    # Launch the app
    demo.launch()