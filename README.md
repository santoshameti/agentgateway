# AI Agent Gateway

## Overview

Agentgateway goal is to get you started with AI agents in the simplest way possible by abstracting out all complexity. This project implements a flexible AI Agent Gateway that supports LLMs from multiple AI backends including OpenAI(GPT and O1), Anthropic (Claude), Bedrock(Claude, Llama, Mistral etc), Groq (Mistral, Llama), Together(Mistral, Llama), Fireworks(Mistral, Llama) and Vertex AI (coming soon). It provides a unified interface for creating and running AI agents with various tools.

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
├── tests/
│   ├── ... (test files)
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
   TOGETHER_API_KEY=your_together_api_key
   FIREWORKS_API_KEY=your_together_api_key
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

1. Create a new file in the `tools/` directory (e.g., `calendar_search_tool.py`).
2. Define a new class that inherits from `Tool` (from `core.abstract_tool`).
3. Implement the required methods: `execute`, `get_parameters_schema`, and `is_auth_setup`.
4. Add any necessary authentication logic.

Example of a hypothetical CalendarSearchTool:

```python
from typing import Dict, Any
from core.abstract_tool import Tool
from some_calendar_api import CalendarAPI  # Hypothetical calendar API

class CalendarSearchTool(Tool):
    def __init__(self):
        super().__init__("calendar_search", "Search for events in a calendar")
        self.api = None

    def is_auth_setup(self):
        return self.api is not None

    def execute(self) -> Any:
        if not self.is_auth_setup():
            raise ValueError("Calendar API not set up. Use set_auth() to set up the API.")
        
        parameters = self.get_parameters()
        start_date = parameters.get('start_date')
        end_date = parameters.get('end_date')
        search_term = parameters.get('search_term')

        events = self.api.search_events(start_date, end_date, search_term)
        return [self.format_event(event) for event in events]

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date for the search (ISO format)"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date for the search (ISO format)"
                },
                "search_term": {
                    "type": "string",
                    "description": "Optional search term to filter events"
                }
            },
            "required": ["start_date", "end_date"]
        }

    def set_auth(self, **kwargs):
        api_key = kwargs.get('api_key')
        if not api_key:
            raise ValueError("API key is required for CalendarSearchTool")
        self.api = CalendarAPI(api_key)

    def format_event(self, event):
        return {
            "title": event.title,
            "start": event.start_time.isoformat(),
            "end": event.end_time.isoformat(),
            "location": event.location
        }
```

To use the new tool:

1. Instantiate the tool: `calendar_tool = CalendarSearchTool()`
2. Set up authentication: `calendar_tool.set_auth(api_key=os.getenv('CALENDAR_API_KEY'))`
3. Add the tool to your agent when creating it:
   ```python
   agent = gateway.create_agent(prompt, tools=[calendar_tool, other_tools...])
   ```

When using the tool, ensure that you handle the tool's parameters correctly in your agent's logic and provide the necessary authentication details.

Remember to import and initialize any required libraries or APIs (in this example, the hypothetical `CalendarAPI`) in your actual implementation.

## Running Tests

To run the tests for this project, follow these steps:

1. Ensure you have pytest installed. If not, install it using:
   ```
   pip install -r requirements.txt
   ```

2. From the root directory of the project (agentgateway), run:
   ```
   python -m pytest
   ```

This command will discover and run all tests in the `tests/` directory, including tests for tools and the tool manager.

To run tests with more detailed output, you can use the `-v` (verbose) flag:
```
python -m pytest -v
```

To see print statements and other output during test execution, use the `-s` flag:
```
python -m pytest -s
```

You can combine these flags for even more detailed output:
```
python -m pytest -v -s
```

To run tests for specific components:

- For all tool tests:
  ```
  python -m pytest tests/tools/
  ```

- For specific tools:
  ```
  python -m pytest tests/tools/test_<tool_name>.py
  ```

- For the tool manager:
  ```
  python -m pytest tests/test_tool_manager.py
  ```

- For all adapter tests:
  ```
  python -m pytest tests/adapters/
  ```

- For specific adapter:
  ```
  python -m pytest tests/tools/test_<adapter_name>.py
  ```
- For the agent gateway:
  ```
  python -m pytest tests/test_agent_gateway.py
   ``` 

Remember to write comprehensive tests for each component to ensure proper functionality and integration.

## Note on Project Structure

Make sure your project structure follows the layout described in this README. The tests expect the tools to be in a module named `agentgateway`, so your directory structure should reflect this.

## Note on Mocking

Some tests, particularly for the WeatherTool and TranslationTool, use mocking to simulate external API calls. This ensures that tests can run without actually making network requests, which makes them faster and more reliable.

When running these tests, make sure you have the `unittest.mock` module available (it's included in Python's standard library for Python 3.3 and newer).


## Continuous Integration

Consider setting up a CI/CD pipeline that runs these tests automatically on each commit or pull request. This will help catch any regressions early in the development process.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Check out our [contribution guidelines](docs/contributing.md).

## License

This project is licensed under the MIT License.
