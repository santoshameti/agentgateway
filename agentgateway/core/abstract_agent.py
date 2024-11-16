import json, os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from agentgateway.core.response import Response
import uuid
from agentgateway.core.abstract_tool import Tool
from agentgateway.core.conversation_manager import ConversationManager
from agentgateway.core.redis_conversation_manager import RedisConversationManager
from agentgateway.core.dynamo_conversation_manager import DynamoConversationManager
from agentgateway.utils.config_manager import ConfigManager


class AbstractAgent(ABC):
    """
    Abstract base class for all agent implementations.
    """
    def __init__(self, model_id: str=""):

        self.config_manager = ConfigManager()
        self.mem_profile = os.environ.get('AGENT_MEMORY_CONFIG_PROFILE', 'default')
        self.model_profile = os.environ.get('AGENT_MODEL_CONFIG_PROFILE', 'default')
        self.instructions = ""
        self.tools = {}
        self.formatted_tools = []
        self.auth_data = {}
        self.model_config = {
            "max_tokens": self.config_manager.get_nested(self.model_profile, 'max_tokens', default=2000),
            "temperature": self.config_manager.get_nested(self.model_profile, 'temperature', default=0.7)
        }
        self.model_id = model_id
        self.current_conversation_id = ""
        self.conversation_manager = self._initialize_conversation_manager()

    def _initialize_conversation_manager(self) -> ConversationManager:
        conversation_manager_type = self.config_manager.get_nested(self.mem_profile, 'conversation_manager',
                                                                   default='in_memory')

        if conversation_manager_type == 'redis':
            redis_url = self.config_manager.get_nested(self.mem_profile, 'redis_url', default='redis://localhost:6379')
            return RedisConversationManager(redis_url)
        elif conversation_manager_type == 'dynamodb':
            table_name = self.config_manager.get_nested(self.mem_profile, 'dynamodb_table', default='conversations')
            region_name = self.config_manager.get_nested(self.mem_profile, 'dynamodb_region', default='us-west-2')
            return DynamoConversationManager(table_name, region_name)
        else:
            return ConversationManager()

    @abstractmethod
    def run(self, agent_input, is_tool_response: Optional[bool] = False, conversation_id: Optional[str] = None) -> Response:
        """
        Execute the agent's main logic and return a response.
        :param tool_response: boolean indicating the type of input
        :param input_message: The input message from the user.
        :return: A dictionary containing the agent's response and metadata.
        """
        if conversation_id is None:
            self.current_conversation_id = str(uuid.uuid4())
            self.clear_conversation_history()
        elif conversation_id != self.current_conversation_id:
            self.current_conversation_id = conversation_id

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


    def get_tool_from_response(self, tool_data: Dict[str, Any]) -> Optional[Tool]:

        tool_name = tool_data.get('name')
        input_params = tool_data.get('input', {})
        if isinstance(input_params, str):
            input_params = json.loads(input_params)
        instance_id = tool_data.get('id')
        tool_instance = None

        if tool_name in self.tools:
            tool_instance = self.tools[tool_name].clone()
            tool_instance.instance_id = instance_id
            self._validate_and_set_input(tool_instance, input_params)

        return tool_instance

    def add_tool(self, tool: Tool):
        """
        Add a new tool to the agent's toolkit.
        :param tool: A Tool instance to be added.
        """
        self.tools[tool.name] = tool

    def remove_tool(self, tool_name: str):
        """
        Remove a tool from the agent's toolkit.
        :param tool_name: The name of the tool to be removed.
        """
        if tool_name in self.tools:
            del self.tools[tool_name]

    def set_model(self, model_id: str):
        self.model_id = model_id

    def get_model(self):
        return self.model_id

    def set_instructions(self, instructions: str):
        """
        Update the agent's prompt.
        :param new_prompt: The new prompt to be used by the agent.
        """
        self.instructions = instructions

    def start_conversation(self) -> str:
        conversation_id = self.conversation_manager.start_conversation()
        self.current_conversation_id = conversation_id
        return conversation_id

    def get_conversation_history(self, conversation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if conversation_id is None:
            conversation_id = self.current_conversation_id
        return self.conversation_manager.get_conversation_history(conversation_id)

    def clear_conversation_history(self, conversation_id: Optional[str] = None):
        if conversation_id is None:
            conversation_id = self.current_conversation_id
        self.conversation_manager.clear_conversation_history(conversation_id)

    def add_to_conversation_history(self, message: Dict[str, Any], conversation_id: Optional[str] = None):
        if conversation_id is None:
            conversation_id = self.current_conversation_id
        self.conversation_manager.add_to_conversation_history(message, conversation_id)

    def extend_conversation_history(self, messages: List, conversation_id: Optional[str] = None):
        if conversation_id is None:
            conversation_id = self.current_conversation_id
        self.conversation_manager.extend_conversation_history(messages, conversation_id)

    def get_formatted_conversation_history(self, conversation_id: Optional[str] = None) -> str:
        if conversation_id is None:
            conversation_id = self.current_conversation_id
        return self.conversation_manager.get_formatted_conversation_history(conversation_id)

    def get_formatted_tool_output(self, tool, tool_output):
        pass

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """
        Get the schema of all tools available to the agent.
        :return: A list of dictionaries representing the tools' schema.
        """
        return [tool.to_dict() for tool in self.tools]

    def _validate_and_set_input(self, tool: Tool, input_params: Dict[str, Any]):
        schema = tool.get_parameters_schema()
        properties = schema.get('properties', {})
        required = schema.get('required', [])

        # Check for required parameters
        for param in required:
            if param not in input_params:
                raise ValueError(f"Missing required parameter: {param}")

        # Validate and set parameters
        for key, value in input_params.items():
            if key not in properties:
                raise ValueError(f"Unexpected parameter: {key}")

            expected_type = properties[key]['type']
            if not self._check_type(value, expected_type):
                raise TypeError(
                    f"Invalid type for parameter '{key}'. Expected {expected_type}, got {type(value).__name__}")

            tool.set_parameter(key, value)

    def _check_type(self, value: Any, expected_type: str) -> bool:
        if expected_type == 'string':
            return isinstance(value, str)
        elif expected_type == 'number':
            return isinstance(value, (int, float))
        elif expected_type == 'integer':
            return isinstance(value, int)
        elif expected_type == 'boolean':
            return isinstance(value, bool)
        elif expected_type == 'array':
            return isinstance(value, list)
        elif expected_type == 'object':
            return isinstance(value, dict)
        else:
            return True

    def _validate_input(self, tool: Tool, input_params: Dict[str, Any]):
        schema = tool.get_parameters_schema()
        required_params = schema.get('required', [])
        properties = schema.get('properties', {})

        # Check for required parameters
        for param in required_params:
            if param not in input_params:
                raise ValueError(f"Missing required parameter: {param}")

        # Check parameter types
        for param, value in input_params.items():
            if param in properties:
                expected_type = properties[param]['type']
                if not self._check_type(value, expected_type):
                    raise TypeError(
                        f"Invalid type for parameter '{param}'. Expected {expected_type}, got {type(value).__name__}")

