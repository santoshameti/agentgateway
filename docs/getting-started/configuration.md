# Configuration Guide

This guide will walk you through the process of configuring the AI Agent Gateway for your environment.

## Environment Variables

The AI Agent Gateway uses environment variables to securely manage API keys and other configuration settings. You'll need to set up these variables before using the gateway.

1. Create a `.env` file in the root directory of the project.
2. Add the following variables to the file, replacing the placeholder values with your actual API keys:

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
TRANSLATION_API_KEY=your_translation_api_key_here
AWS_ACCESS_API=your_aws_api_key
AWS_SECRET_KEY=your_aws_secret_access_key
AWS_REGION_ID=your_aws_region
TOGETHER_API_KEY=your_together_api_key
FIREWORKS_API_KEY=your_fireworks_api_key
```

## Loading Environment Variables

In your Python script, use the `dotenv` library to load these environment variables:

```python
from dotenv import load_dotenv

load_dotenv()
```

## Configuring AI Backends

The AI Agent Gateway supports multiple AI backends. You can configure which backend to use when initializing the `AgentGateway` class:

```python
from agent_gateway import AgentGateway, AgentType

# For OpenAI
gateway = AgentGateway(AgentType.OPENAI, model_id="gpt-3.5-turbo")

# For Anthropic
gateway = AgentGateway(AgentType.ANTHROPIC, model_id="claude-3-5-sonnet-20240620")

# For Bedrock
gateway = AgentGateway(AgentType.BEDROCK, model_id="your_bedrock_model_id")

# For Vertex AI (coming soon)
# gateway = AgentGateway(AgentType.VERTEX, model_id="your_vertex_model_id")
```

## Configuring Tools

To use tools with your agent, you need to initialize them and set up their authentication:

```python
from tools.weather_tool import WeatherTool
from tools.translate_tool import TranslationTool

weather_tool = WeatherTool()
translation_tool = TranslationTool()

weather_tool.set_auth(api_key=os.getenv('WEATHER_API_KEY'))
translation_tool.set_auth(api_key=os.getenv('TRANSLATION_API_KEY'))
```

## Next Steps

Now that you've configured your environment, you're ready to start using the AI Agent Gateway. Check out the [Quick Start Guide](quick-start.md) for a simple example of how to create and run an agent.
