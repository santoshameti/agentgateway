# Advanced Scenarios Examples

This guide showcases more complex uses of the AI Agent Gateway.

## Example 1: Multi-turn Conversation with Tool Usage

```python
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt
from tools import WeatherTool, CalculatorTool

gateway = AgentGateway(AgentType.OPENAI)
gateway.adapter.set_auth(api_key="your_openai_api_key_here")

weather_tool = WeatherTool()
weather_tool.set_auth(api_key="your_weather_api_key_here")
calculator_tool = CalculatorTool()

prompt = Prompt("You are a helpful assistant that can provide weather information and perform calculations.")
agent = gateway.create_agent(prompt, tools=[weather_tool, calculator_tool])

conversation = [
    "What's the weather like in London?",
    "If the temperature in London is 20°C, what would it be in Fahrenheit?",
    "What's the square root of that Fahrenheit temperature?"
]

for user_input in conversation:
    response = gateway.run_agent(agent, user_input)
    print(f"User: {user_input}")
    print(f"Assistant: {response.content}\n")
```

## Example 2: Custom Tool Integration

```python
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt
from core.abstract_tool import Tool

class StockPriceTool(Tool):
    def __init__(self):
        super().__init__("stock_price", "Get the current stock price for a given symbol")

    def execute(self):
        # Simulated stock price retrieval
        symbol = self.get_parameter("symbol")
        return f"The current stock price for {symbol} is $150.25"

    def get_parameters_schema(self):
        return {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL)"}
            },
            "required": ["symbol"]
        }

    def is_auth_setup(self):
        return True  # No auth required for this example

gateway = AgentGateway(AgentType.ANTHROPIC)
gateway.adapter.set_auth(api_key="your_anthropic_api_key_here")

stock_tool = StockPriceTool()

prompt = Prompt("You are a financial advisor that can provide stock price information.")
agent = gateway.create_agent(prompt, tools=[stock_tool])

response = gateway.run_agent(agent, "What's the current stock price of Apple?")
print(response.content)
```

These advanced examples demonstrate how to use the AI Agent Gateway for multi-turn conversations, tool chaining, and integrating custom tools. You can further expand on these concepts to build sophisticated AI-powered applications.
