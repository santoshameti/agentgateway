from enum import Enum
from typing import Optional, Any, List, Dict


class ResponseType(Enum):
    ANSWER = "answer"
    TOOL_CALL = "tool_use"
    ASK_USER = "ask_user"
    ERROR = "error"

class EventType(Enum):
    LLM_CALL = "llm_call"
    TOOL_CALL = "tool_call"

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
        self.trace_details = [] # List to store individual call metrics

    def __str__(self):
        return (f"Response(type={self.response_type.value}, content={self.content}, "
                f"conversation_id={self.conversation_id}), usage={self.get_usage_details()}, "
                f"trace={self.trace_details}")

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

    def add_trace_detail(self, event_type: 'EventType', latency: Optional[float] = None,
                         input_tokens: Optional[int] = None, output_tokens: Optional[int] = None,
                         name: Optional[str] = None, start_time: Optional[str] = None,
                         end_time: Optional[str] = None):
        """
        Adds a trace detail if at least one metric is provided.

        :param event_type: The type of event (LLM_CALL or TOOL_CALL).
        :param latency: Time taken for the call in seconds.
        :param input_tokens: Number of input tokens for the call.
        :param output_tokens: Number of output tokens for the call.
        :param name: Name of the event (e.g., tool name).
        :param start_time: Optional start time of the event (ISO 8601 string).
        :param end_time: Optional end time of the event (ISO 8601 string).
        """
        if event_type and (latency is not None or input_tokens is not None or
                           output_tokens is not None or name is not None or
                           start_time is not None or end_time is not None):
            detail = {
                "event_type": event_type.value,
                "latency": latency,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "name": name,
                "start_time": start_time,
                "end_time": end_time
            }
            self.trace_details.append(detail)

    def get_trace_details(self) -> List[Dict[str, Any]]:
        """
        Returns the trace details.

        :return: A list of dictionaries containing trace metrics.
        """
        return self.trace_details

    def to_dict(self):
        return {
            "type": self.response_type.value,
            "content": self.content,
            "tools": self.tools,
            "conversation_id": self.conversation_id,
            "llm_usage": self.get_usage_details(),
            "trace_details": self.trace_details,
        }

