import copy
from abc import ABC, abstractmethod
from typing import Dict, Any


class Tool(ABC):
    """
    Abstract base class for all tool implementations.
    """

    def __init__(self, name: str, description: str):
        """
        Initialize the tool with a name and description.
        :param name: The name of the tool.
        :param description: A brief description of what the tool does.
        """
        self.name = name
        self.instance_id = ""
        self.description = description
        self.auth_data = {}
        self._parameters: Dict[str, Any] = {}

    @abstractmethod
    def execute(self) -> Any:
        """
        Execute the tool's functionality.
        :param parameters: A dictionary of parameters required by the tool.
        :return: The result of the tool's execution.
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tool to a dictionary representation.
        :return: A dictionary containing the tool's schema.
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.get_parameters_schema()
            }
        }

    @abstractmethod
    def get_parameters_schema(self) -> Dict[str, Any]:
        """
        Get the JSON schema for the tool's parameters.
        :return: A dictionary representing the JSON schema of the tool's parameters.
        """
        pass

    def set_auth(self, **kwargs):
        self.auth_data.update(kwargs)

    def get_auth(self) -> Dict[str, Any]:
        return self.auth_data
        #return {k: '********' if k.lower().endswith('key') else v for k, v in self.auth_data.items()}

    @abstractmethod
    def is_auth_setup(self) -> bool:
        pass

    def set_parameters(self, parameters: Dict[str, Any]):
        """
        Set the parameters for the tool.
        :param parameters: A dictionary of parameters to set.
        """
        schema = self.get_parameters_schema()
        properties = schema.get('properties', {})
        required = schema.get('required', [])

        for key, value in parameters.items():
            if key not in properties:
                raise ValueError(f"Unexpected parameter: {key}")
            if key in required and value is None:
                raise ValueError(f"Required parameter '{key}' cannot be None")
            self._parameters[key] = value

        # Check if all required parameters are set
        for req in required:
            if req not in self._parameters:
                raise ValueError(f"Missing required parameter: {req}")

    def get_parameters(self) -> Dict[str, Any]:
        """
        Get the current parameters of the tool.
        :return: A dictionary of the tool's parameters.
        """
        return self._parameters.copy()

    def get_parameter(self, key: str) -> Any:
        """
        Get a specific parameter by key.
        :param key: The key of the parameter to retrieve.
        :return: The value of the specified parameter.
        :raises KeyError: If the parameter key does not exist.
        """
        if key not in self._parameters:
            raise KeyError(f"Parameter '{key}' not found")
        return self._parameters[key]

    def set_parameter(self, key: str, value: Any):
        """
        Set a specific parameter by key.
        :param key: The key of the parameter to set.
        :param value: The value to set for the parameter.
        :raises ValueError: If the parameter is not defined in the schema or if it's a required parameter and the value is None.
        """
        schema = self.get_parameters_schema()
        properties = schema.get('properties', {})
        required = schema.get('required', [])

        if key not in properties:
            raise ValueError(f"Unexpected parameter: {key}")
        if key in required and value is None:
            raise ValueError(f"Required parameter '{key}' cannot be None")

        self._parameters[key] = value

    def set_instance_id(self, instance_id: str):
        self.instance_id = instance_id

    def get_instance_id(self) -> str:
        return self.instance_id

    def get_name(self) -> str:
        return self.name

    def clone(self):
        """
        Create a deep copy of the tool.
        :return: A new instance of the tool with copied attributes.
        """
        new_tool = copy.deepcopy(self)
        # Reset or reinitialize certain attributes as needed
        new_tool.instance_id = ""
        return new_tool

