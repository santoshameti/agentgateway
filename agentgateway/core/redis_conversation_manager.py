import redis
import json
from typing import List, Dict, Any, Optional
import uuid
from agentgateway.core.conversation_manager import ConversationManager


class RedisConversationManager(ConversationManager):
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    def start_conversation(self) -> str:
        conversation_id = str(uuid.uuid4())
        self.redis.set(f"conversation:{conversation_id}", json.dumps([]))
        return conversation_id

    def get_conversation_history(self, conversation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")
        return json.loads(self.redis.get(f"conversation:{conversation_id}") or "[]")

    def clear_conversation_history(self, conversation_id: Optional[str] = None):
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")
        else:
            self.redis.delete(f"conversation:{conversation_id}")

    def add_to_conversation_history(self, message: Dict[str, Any], conversation_id: Optional[str] = None):
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")
        history = self.get_conversation_history(conversation_id)
        history.append(message)
        self.redis.set(f"conversation:{conversation_id}", json.dumps(history))

    def extend_conversation_history(self, messages: List, conversation_id: Optional[str] = None):
        if conversation_id is None:
            raise ValueError("Conversation ID cannot be None")
        history = self.get_conversation_history(conversation_id)
        history.extend(messages)
        self.redis.set(f"conversation:{conversation_id}", json.dumps(history))

    def get_formatted_conversation_history(self, conversation_id: Optional[str] = None) -> str:
        history = self.get_conversation_history(conversation_id)
        formatted_history = ""
        for message in history:
            formatted_history += f"{message['role'].capitalize()}: {message['content']}\n"
        return formatted_history.strip()