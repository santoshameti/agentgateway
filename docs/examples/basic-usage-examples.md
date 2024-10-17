# Basic Usage Examples

This guide provides simple examples to help you get started with the AI Agent Gateway.

## Example 1: Creating and Running a Simple Agent

```python
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt

# Initialize the Agent Gateway
gateway = AgentGateway(AgentType.OPENAI)

# Set up authentication
gateway.adapter.set_auth(api_key="your_openai_api_key_here")

# Create a prompt
prompt = Prompt("You are a helpful assistant that answers questions about science.")

# Create an agent
agent = gateway.create_agent(prompt)

# Run the agent
response = gateway.run_agent(agent, "What is photosynthesis?")
print(response.content)
```

## Example 2: Using a Built-in Tool

```python
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt
from tools import WeatherTool

# Initialize the Agent Gateway
gateway = AgentGateway(AgentType.ANTHROPIC)

# Set up authentication
gateway.adapter.set_auth(api_key="your_anthropic_api_key_here")

# Create and authenticate the Weather Tool
weather_tool = WeatherTool()
weather_tool.set_auth(api_key="your_weather_api_key_here")

# Create a prompt
prompt = Prompt("You are a helpful assistant that can provide weather information.")

# Create an agent with the Weather Tool
agent = gateway.create_agent(prompt, tools=[weather_tool])

# Run the agent
response = gateway.run_agent(agent, "What's the weather like in New York?")
print(response.content)
```

These examples demonstrate the basic usage of the AI Agent Gateway with different AI backends and tools. You can build upon these examples to create more complex applications.
