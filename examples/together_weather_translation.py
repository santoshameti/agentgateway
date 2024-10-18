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
gateway = AgentGateway(AgentType.TOGETHER, model_id="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo")

# Set up Anthropic authentication
gateway.adapter.set_auth(api_key=os.getenv('TOGETHER_API_KEY'))

# Set the prompt for Agent with the necessary instructions
prompt = Prompt("You are a helpful assistant that can access external functions. The responses from these function calls will be appended to this dialogue. Please provide responses based on the information from these function calls.If you need to get input from the user, use ask user tool, do not assume parameters.")
gateway.prepare_agent(prompt, tools=[translation_tool, weather_tool, ask_tool])

agent_input_1tool = "Translate 'Hello, how are you?' to German"
agent_input_2tools = "Translate 'Hello, how are you?' to Spanish and tell me the weather in Madrid"
agent_input_no_params = "Get me the current weather please"
multiple_inputs = "Translate to Hindi and Get me weather"

try:
    gateway.start_conversation()
    result_1 = gateway.run_agent(agent_input_1tool)
    print(result_1)
    gateway.start_conversation()
    result_2 = gateway.run_agent(agent_input_2tools)
    print(result_2)
    gateway.start_conversation()
    result_3 = gateway.run_agent(agent_input_no_params)
    print(result_3)
#    result_4 = gateway.run_agent(multiple_inputs)
#    print(f" Agent input: {multiple_inputs}, Agent output: {result_4}")
except Exception as e:
    print(str(e))

