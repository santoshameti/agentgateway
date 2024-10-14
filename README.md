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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
