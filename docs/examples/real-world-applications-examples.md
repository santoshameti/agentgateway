# Real-world Applications Examples

This guide presents examples of how the AI Agent Gateway can be used in real-world scenarios.

## Example 1: Customer Support Chatbot

```python
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt
from tools import TranslationTool, AskUserTool

class ProductDatabaseTool(Tool):
    # Implement a tool to query product information
    pass

class OrderStatusTool(Tool):
    # Implement a tool to check order status
    pass

gateway = AgentGateway(AgentType.OPENAI)
gateway.adapter.set_auth(api_key="your_openai_api_key_here")

translation_tool = TranslationTool()
translation_tool.set_auth(api_key="your_translation_api_key_here")
ask_user_tool = AskUserTool()
product_db_tool = ProductDatabaseTool()
order_status_tool = OrderStatusTool()

prompt = Prompt("""
You are a customer support chatbot. You can help with product information, 
order status, and general inquiries. You can communicate in multiple languages 
and ask for clarification when needed.
""")

agent = gateway.create_agent(prompt, tools=[
    translation_tool, ask_user_tool, product_db_tool, order_status_tool
])

def chat_loop():
    print("Customer Support Chatbot: Hello! How can I assist you today?")
    while True:
        user_input = input("Customer: ")
        if user_input.lower() == "exit":
            break
        response = gateway.run_agent(agent, user_input)
        print(f"Customer Support Chatbot: {response.content}")

chat_loop()
```

## Example 2: Data Analysis Assistant

```python
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt
from tools import CalculatorTool

class DataVisualizationTool(Tool):
    # Implement a tool to create data visualizations
    pass

class DataQueryTool(Tool):
    # Implement a tool to query a database or data file
    pass

gateway = AgentGateway(AgentType.ANTHROPIC)
gateway.adapter.set_auth(api_key="your_anthropic_api_key_here")

calculator_tool = CalculatorTool()
data_viz_tool = DataVisualizationTool()
data_query_tool = DataQueryTool()

prompt = Prompt("""
You are a data analysis assistant. You can help with querying data, 
performing calculations, and creating visualizations. Provide clear 
explanations of your analysis process and findings.
""")

agent = gateway.create_agent(prompt, tools=[
    calculator_tool, data_viz_tool, data_query_tool
])

def analyze_data():
    print("Data Analysis Assistant: Hello! What would you like to analyze today?")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        response = gateway.run_agent(agent, user_input)
        print(f"Data Analysis Assistant: {response.content}")

analyze_data()
```

These real-world application examples demonstrate how the AI Agent Gateway can be used to create sophisticated AI-powered systems for customer support and data analysis. You can adapt and expand these examples to suit various business needs and use cases.
