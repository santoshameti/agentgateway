from enum import Enum
from typing import Optional, Any

class ResponseType(Enum):
    ANSWER = "answer"
    TOOL_CALL = "tool_use"
    ASK_USER = "ask_user"
    ERROR = "error"

class Response:
    def __init__(self, 
                 response_type: 'ResponseType' = None,
                 content: str = None,
                 conversation_id: Optional[str] = None
                 ):
        self.response_type = response_type
        self.content = content
        self.conversation_id = conversation_id
        self.tools = []
        self.llm_calls = 0  # Tracks the number of LLM calls
        self.total_input_tokens = 0  # Tracks total input tokens
        self.total_output_tokens = 0  # Tracks total output tokens

    def __str__(self):
        return (f"Response(type={self.response_type.value}, content={self.content}, "
                f"conversation_id={self.conversation_id}), usage={self.get_usage_details()}")

    def set_response_type(self, response_type: 'ResponseType'):
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

    def update_usage(self, input_tokens: int, output_tokens: int):
        """
        Updates the LLM usage details.

        :param input_tokens: Number of tokens in the input for the call.
        :param output_tokens: Number of tokens in the output for the call.
        """
        self.llm_calls += 1
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

    def get_usage_details(self):
        """
        Returns the LLM usage details.

        :return: A dictionary containing usage details.
        """
        return {
            "llm_calls": self.llm_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
        }

    def to_dict(self):
        return {
            "type": self.response_type.value,
            "content": self.content,
            "tools": self.tools,
            "conversation_id": self.conversation_id,
            "llm_usage": self.get_usage_details(),
        }

