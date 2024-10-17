# Quick Start Guide

This guide will help you quickly set up and run your first AI agent using the AI Agent Gateway.

## Prerequisites

Ensure you have completed the [Installation](installation.md) and [Configuration](configuration.md) steps.

## Step 1: Import Required Modules

```python
import os
from dotenv import load_dotenv
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt
from tools.weather_tool import WeatherTool
from tools.translate_tool import TranslationTool
```

## Step 2: Load Environment Variables

```python
load_dotenv()
```

## Step 3: Create and Configure Tools

```python
translation_tool = TranslationTool()
weather_tool = WeatherTool()

translation_tool.set_auth(api_key=os.getenv('TRANSLATION_API_KEY'))
weather_tool.set_auth(api_key=os.getenv('WEATHER_API_KEY'))
```

## Step 4: Create the Agent Gateway

```python
gateway = AgentGateway(AgentType.ANTHROPIC, model_id="claude-3-5-sonnet-20240620")
gateway.adapter.set_auth(api_key=os.getenv('ANTHROPIC_API_KEY'))
```

## Step 5: Set Up the Agent Prompt

```python
prompt = Prompt("You are a helpful assistant that can translate text and provide weather information. Use the relevant tools as needed, do not respond from memory. When the required answers are available, summarize the response and provide an answer.")
```

## Step 6: Prepare the Agent

```python
gateway.prepare_agent(prompt, tools=[translation_tool, weather_tool])
```

## Step 7: Run the Agent

```python
agent_input = "Translate 'Hello, how are you?' to Spanish and tell me the weather in Madrid"

try:
    result = gateway.run_agent(agent_input)
    print(result)
except Exception as e:
    print(str(e))
```

## Complete Example

Here's the complete script that puts all these steps together:

```python
import os
from dotenv import load_dotenv
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt
from tools.weather_tool import WeatherTool
from tools.translate_tool import TranslationTool

# Load environment variables
load_dotenv()

# Create and configure tools
translation_tool = TranslationTool()
weather_tool = WeatherTool()
translation_tool.set_auth(api_key=os.getenv('TRANSLATION_API_KEY'))
weather_tool.set_auth(api_key=os.getenv('WEATHER_API_KEY'))

# Create the agent gateway
gateway = AgentGateway(AgentType.ANTHROPIC, model_id="claude-3-5-sonnet-20240620")
gateway.adapter.set_auth(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Set up the agent prompt
prompt = Prompt("You are a helpful assistant that can translate text and provide weather information. Use the relevant tools as needed, do not respond from memory. When the required answers are available, summarize the response and provide an answer.")

# Prepare the agent
gateway.prepare_agent(prompt, tools=[translation_tool, weather_tool])

# Run the agent
agent_input = "Translate 'Hello, how are you?' to Spanish and tell me the weather in Madrid"

try:
    result = gateway.run_agent(agent_input)
    print(result)
except Exception as e:
    print(str(e))
```

This script sets up an AI agent that can translate text and provide weather information. It then asks the agent to translate a phrase to Spanish and provide the weather in Madrid.

## Next Steps

Now that you've run your first agent, you can explore more complex scenarios by:

1. Adding more tools to your agent
2. Trying different AI backends
3. Experimenting with different prompts

Check out the [Core Concepts](../core-concepts/agent-gateway.md) section to deepen your understanding of how the AI Agent Gateway works.
