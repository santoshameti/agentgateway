from typing import List, Dict, Any, Optional
import uuid

class ConversationManager:
    def __init__(self):
        self.conversations = {}

    def start_conversation(self) -> str:
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = []
        return conversation_id

    def get_conversation_history(self, conversation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")

        return self.conversations.get(conversation_id, [])

    def clear_conversation_history(self, conversation_id: Optional[str] = None):
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")
        else:
            self.conversations.pop(conversation_id, None)

    def add_to_conversation_history(self, message: Dict[str, Any], conversation_id: Optional[str] = None):
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")
        self.conversations.setdefault(conversation_id, []).append(message)

    def extend_conversation_history(self, messages: List, conversation_id: Optional[str] = None):
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")

        self.conversations.setdefault(conversation_id, []).extend(messages)

    def get_formatted_conversation_history(self, conversation_id: Optional[str] = None) -> str:
        history = self.get_conversation_history(conversation_id)
        formatted_history = ""
        for message in history:
            formatted_history += f"{message['role'].capitalize()}: {message['content']}\n"
        return formatted_history.strip()