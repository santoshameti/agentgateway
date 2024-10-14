from abc import ABC, abstractmethod
from typing import List, Dict, Any
from core.response import Response

from anthropic.types import Model

from .abstract_tool import Tool

class AbstractAgent(ABC):
    """
    Abstract base class for all agent implementations.
    """
    def __init__(self, model_id: str=""):

        self.instructions = ""
        self.tools = []
        self.formatted_tools = []
        self.conversation_history = []
        self.auth_data = {}
        self.model_config = {
            "max_tokens": 2000,
            "temperature": 0.7
        }
        self.model_id = model_id

    @abstractmethod
    def run(self, agent_input, is_tool_response) -> Response:
        """
        Execute the agent's main logic and return a response.
        :param tool_response: boolean indicating the type of input
        :param input_message: The input message from the user.
        :return: A dictionary containing the agent's response and metadata.
        """
        pass

    @abstractmethod
    def set_auth(self, **kwargs):
        """
        Set the authentication data for the agent.
        :param kwargs: Key-value pairs of authentication data.
        """
        pass

    @abstractmethod
    def get_auth(self) -> Dict[str, Any]:
        """
        Get the current authentication data.
        :return: A dictionary containing the current authentication data.
        """
        pass

    @abstractmethod
    def set_model_config(self, **kwargs):
        """
        Set or update the model configuration.
        :param kwargs: Key-value pairs of model configuration.
        """
        pass

    @abstractmethod
    def get_model_config(self) -> Dict[str, Any]:
        """
        Get the current model configuration.
        :return: A dictionary containing the current model configuration.
        """
        pass

    def add_tool(self, tool: Tool):
        """
        Add a new tool to the agent's toolkit.
        :param tool: A Tool instance to be added.
        """
        self.tools.append(tool)

    def remove_tool(self, tool_name: str):
        """
        Remove a tool from the agent's toolkit.
        :param tool_name: The name of the tool to be removed.
        """
        self.tools = [tool for tool in self.tools if tool.name != tool_name]

    def set_model(self, model_id: str):
        self.model_id = model_id

    def get_model(self, model_id: str):
        return self.model_id

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """
        Execute a specific tool with the given parameters.
        :param tool_name: The name of the tool to execute.
        :param parameters: The parameters to pass to the tool.
        :return: The result of the tool execution.
        """
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.execute(parameters)
        raise ValueError(f"Tool '{tool_name}' not found")

    def set_instructions(self, instructions: str):
        """
        Update the agent's prompt.
        :param new_prompt: The new prompt to be used by the agent.
        """
        self.instructions = instructions

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Retrieve the conversation history.
        :return: A list of dictionaries containing the conversation history.
        """
        return self.conversation_history

    def clear_conversation_history(self):
        """
        Clear the conversation history.
        """
        self.conversation_history = []

    def add_to_conversation_history(self, role: str, content):
        """
        Add a new message to the conversation history.
        :param role: The role of the message sender (e.g., "user", "assistant", "system").
        :param content: The content of the message.
        """
        self.conversation_history.append({"role": role, "content": content})

    def get_formatted_tool_output(self, id, tool_output):
        pass
    def get_formatted_conversation_history(self) -> str:
        """
        Get the conversation history formatted as a string for model input.
        :return: A formatted string representation of the conversation history.
        """
        formatted_history = ""
        for message in self.conversation_history:
            formatted_history += f"{message['role'].capitalize()}: {message['content']}\n"
        return formatted_history.strip()

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """
        Get the schema of all tools available to the agent.
        :return: A list of dictionaries representing the tools' schema.
        """
        return [tool.to_dict() for tool in self.tools]