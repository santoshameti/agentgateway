# Tools

Tools in the AI Agent Gateway system are modular components that extend the capabilities of agents. They allow agents to perform specific tasks or access external information sources. Tools are designed to be easily integrated into agents and can be dynamically added or removed as needed.

## Tool Structure

A tool consists of the following key components:

1. **Name**: A unique identifier for the tool.
2. **Description**: A brief explanation of what the tool does.
3. **Parameters**: The input parameters required by the tool.
4. **Execution Logic**: The actual functionality of the tool.
5. **Authentication**: (Optional) Mechanism for securely accessing external services.

## Abstract Tool

The `AbstractTool` class serves as the base class for all tool implementations. It defines the common interface and functionality that all tools should have.

### Properties

- `name`: The unique name of the tool.
- `description`: A brief description of the tool's functionality.

### Methods

#### `__init__(self, name: str, description: str)`
Initializes a new tool with the given name and description.

#### `execute(self) -> Any`
Executes the tool's main functionality. This is an abstract method that must be implemented by subclasses.

#### `get_parameters_schema(self) -> Dict[str, Any]`
Returns a JSON schema describing the parameters required by the tool. This is an abstract method that must be implemented by subclasses.

#### `is_auth_setup(self) -> bool`
Checks if the tool's authentication is properly set up. This is an abstract method that must be implemented by subclasses.

#### `set_auth(self, **kwargs)`
Sets up authentication for the tool. This method should be implemented by subclasses that require authentication.

#### `get_auth(self) -> Dict[str, Any]`
Returns the current authentication settings for the tool. This method should be implemented by subclasses that require authentication.

## Creating Custom Tools

To create a new tool:

1. Create a new class that inherits from `AbstractTool`.
2. Implement the required abstract methods: `execute`, `get_parameters_schema`, and `is_auth_setup`.
3. If the tool requires authentication, implement `set_auth` and `get_auth` methods.
4. Add any additional methods or properties specific to your tool.

Example of a custom weather tool:

```python
from core.abstract_tool import AbstractTool
from typing import Dict, Any
import requests

class WeatherTool(AbstractTool):
    def __init__(self):
        super().__init__("weather", "Get current weather information for a location")
        self.api_key = None

    def execute(self) -> Any:
        if not self.is_auth_setup():
            raise ValueError("Weather API key not set")
        
        location = self.get_parameters().get('location')
        url = f"https://api.weatherservice.com/current?location={location}&apikey={self.api_key}"
        response = requests.get(url)
        return response.json()

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and country for which to fetch weather information"
                }
            },
            "required": ["location"]
        }

    def is_auth_setup(self) -> bool:
        return self.api_key is not None

    def set_auth(self, **kwargs):
        self.api_key = kwargs.get('api_key')
        if not self.api_key:
            raise ValueError("API key is required for WeatherTool")

    def get_auth(self) -> Dict[str, Any]:
        return {"api_key": self.api_key}
```

## Using Tools with Agents

To use a tool with an agent:

1. Create an instance of the tool.
2. Set up any required authentication for the tool.
3. Add the tool to the agent using the `add_tool` method.

Example:

```python
from agent_gateway import AgentGateway, AgentType
from tools.weather_tool import WeatherTool

# Create and configure the tool
weather_tool = WeatherTool()
weather_tool.set_auth(api_key="your_api_key_here")

# Create the agent gateway and add the tool
gateway = AgentGateway(AgentType.OPENAI, model_id="gpt-3.5-turbo")
gateway.prepare_agent(prompt, tools=[weather_tool])

# Now the agent can use the weather tool when processing user inputs
```

By creating custom tools, you can significantly extend the capabilities of your AI agents, allowing them to interact with external services, databases, or perform complex calculations.
