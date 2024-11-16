from enum import Enum
from typing import Optional, Any

class ResponseType(Enum):
    ANSWER = "answer"
    TOOL_CALL = "tool_use"
    ASK_USER = "ask_user"
    ERROR = "error"

class Response:
    def __init__(self, 
                 response_type: ResponseType = None,
                 content: str = None,
                 conversation_id: Optional[str] = None
                 ):
        self.response_type = response_type
        self.content = content
        self.conversation_id = conversation_id
        self.tools = []

    def __str__(self):
        return f"Response(type={self.response_type.value}, content={self.content})"

    def set_response_type(self, response_type: ResponseType):
        self.response_type = response_type

    def set_content(self, content: str):
        self.content = content

    def get_tools(self):
        return self.tools

    def set_tools(self, tools: list):
        self.tools = tools

    def get_conversation_id(self) -> Optional[str]:
        return self.conversation_id

    def set_conversation_id(self, conversation_id: str):
        self.conversation_id = conversation_id

    def to_dict(self):
        return {
            "type": self.response_type.value,
            "content": self.content,
            "tools": self.tools,
            "conversation_id": self.conversation_id
        }
