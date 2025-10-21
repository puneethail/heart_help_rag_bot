import json
import os
from src.constants.prompt import prompt_data

# Function to construct the complete system prompt from JSON
def construct_prompt(prompt_data:str = prompt_data ,query : str = None, context:str= None, chat_history:str = None):
    """
    Constructs a comprehensive prompt string from the JSON dictionary.
    """
    knowledgebase = {
        "context" : context,
        "chat_history" : chat_history
    }

    
    prompt = (
        f"[SYSTEM]\n{prompt_data}\n\n"
        f"[KNOWLEDEBASE]\n{knowledgebase}\n\n"
        f"[USER_QUERRY ]\n{query}"
    )
    
    
    
    return prompt

json_prompt = construct_prompt(query= "Hey1", context= "hey heyh heyy", chat_history= "hey_2")


