from collections import deque

class ConversationHistory:
    def __init__(self, max_history=10):
        self.history = deque(maxlen=max_history)
    
    def add_exchange(self, user_query, assistant_response):
        self.history.append({
            "user": user_query,
            "assistant": assistant_response
        })
    
    def get_history_string(self):
        """Format history for LLM context"""
        history_text = ""
        for exchange in self.history:
            history_text += f"User: {exchange['user']}\nAssistant: {exchange['assistant']}\n\n"
        return history_text
    
    def clear(self):
        self.history.clear()
