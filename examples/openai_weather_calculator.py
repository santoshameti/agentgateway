import os
from dotenv import load_dotenv
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt
from tools.weather_tool import WeatherTool
from tools.translate_tool import TranslationTool
from tools.askuser_tool import AskUserTool

# Load environment variables
load_dotenv()

# create the tools needed for the agent
translation_tool = TranslationTool()
weather_tool = WeatherTool()
ask_tool = AskUserTool()

# Set up tool authentication from the .env files
translation_tool.set_auth(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Create the agent gateway
gateway = AgentGateway(AgentType.OPENAI, model_id="gpt-4o")

# Set up Anthropic authentication
gateway.adapter.set_auth(api_key=os.getenv('OPENAI_API_KEY'))

# Set the prompt for Agent with the necessary instructions
prompt = Prompt("You are a helpful assistant that can translate text and provide weather information. Use the relevant tools as needed, do not respond from memory. Use the ask user function or tool any number of times to get input from the user to perform the task. Do not use stop reason to ask questions from the user. When the required answers are available, summarize the response and provide an answer.")
gateway.prepare_agent(prompt, tools=[translation_tool, weather_tool, ask_tool])

agent_input_1tool = "Translate 'Hello, how are you?' to German"
agent_input_2tools = "Translate 'Hello, how are you?' to Spanish and tell me the weather in Madrid"
agent_input_no_params = "Get me weather please"
multiple_inputs = "Translate to Hindi and Get me weather"

try:
#    result_1 = gateway.run_agent(agent_input_1tool)
#    print(f" Agent input: {agent_input_1tool}, Agent output: {result_1}")
#    result_2 = gateway.run_agent(agent_input_2tools)
#    print(f" Agent input: {agent_input_2tools}, Agent output: {result_2}")
#    result_3 = gateway.run_agent(agent_input_no_params)
#    print(f" Agent input: {agent_input_no_params}, Agent output: {result_3}")
    result_4 = gateway.run_agent(multiple_inputs)
    print(f" Agent input: {multiple_inputs}, Agent output: {result_4}")
except Exception as e:
    print(str(e))

