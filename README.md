# AI Agent Gateway

## Overview

This project implements a flexible AI Agent Gateway that supports multiple AI backends including OpenAI, Anthropic (Claude), Bedrock, and Vertex AI (coming soon). It provides a unified interface for creating and running AI agents with various tools.

## Features

- Support for multiple AI backends (OpenAI, Anthropic, Bedrock, Vertex AI)
- Extensible tool system with built-in tools for weather, calculations, and translations
- Secure management of API keys using environment variables
- Easy-to-use interface for creating and running AI agents

## Project Structure

```
.
├── agent_gateway.py
├── core/
│   ├── __init__.py
│   ├── abstract_agent.py
│   ├── agent.py
│   ├── prompt.py
│   ├── response.py
│   └── abstract_tool.py
├── adapters/
│   ├── __init__.py
│   ├── anthropic_claude_adapter.py
│   ├── openai_gpt_adapter.py
│   ├── bedrock_converse_adapter.py
│   └── ... (other adapter files)
├── tools/
│   ├── __init__.py
│   ├── ask_user_tool.py
│   ├── weather_tool.py
│   ├── calculator_tool.py
│   └── translation_tool.py
├── examples/
│   ├── openai_example.py
│   ├── bedrock_example.py
│   └── anthropic_example.py
├── .env
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-agent-gateway.git
   cd ai-agent-gateway
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   WEATHER_API_KEY=your_weather_api_key_here
   TRANSLATION_API_KEY=your_translation_api_key_here
   AWS_ACCESS_API=your_aws_api_key
   AWS_SECRET_KEY=your_aws_secret_access_key
   AWS_REGION_ID=your_aws_region
   ```

## Usage

Here's a basic example of how to use the AI Agent Gateway with OpenAI:

```python
import os
from dotenv import load_dotenv
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt
from tools import WeatherTool, CalculatorTool

# Load environment variables
load_dotenv()

# Create the tools
weather_tool = WeatherTool()
calculator_tool = CalculatorTool()

# Set up tool authentication
weather_tool.set_auth(api_key=os.getenv('WEATHER_API_KEY'))

# Create the agent gateway
gateway = AgentGateway(AgentType.OPENAI)

# Set up OpenAI authentication
gateway.adapter.set_auth(api_key=os.getenv('OPENAI_API_KEY'))

# Create the agent
prompt = Prompt("You are a helpful assistant that can provide weather information and perform calculations.")
agent = gateway.create_agent(prompt, tools=[weather_tool, calculator_tool])

# Run the agent
result = gateway.run_agent(agent, "What's the weather like in London and what's 15 * 24?")
print(result)
```

For more examples, check the `examples/` directory.

## Adding New Tools

To add a new tool:

1. Create a new file in the `tools/` directory (e.g., `my_new_tool.py`).
2. Define a new class that inherits from `AuthenticatedTool`.
3. Implement the `execute` and `get_parameters_schema` methods.
4. Add any necessary authentication logic in the `set_auth` method.

Example:

```python
from typing import Dict, Any
from .authenticated_tool import AuthenticatedTool

class MyNewTool(AuthenticatedTool):
    def __init__(self):
        super().__init__("my_new_tool", "Description of what my new tool does")

    def execute(self, parameters: Dict[str, Any]) -> Any:
        # Implement the tool's functionality here
        pass

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "Description of param1"},
                "param2": {"type": "integer", "description": "Description of param2"}
            },
            "required": ["param1", "param2"]
        }

    def set_auth(self, **kwargs):
        # Implement any necessary authentication logic here
        pass
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
