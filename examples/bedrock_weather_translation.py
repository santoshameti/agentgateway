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
gateway = AgentGateway(AgentType.BEDROCK, model_id="anthropic.claude-3-sonnet-20240229-v1:0")


aws_access_key_id = os.getenv('AWS_ACCESS_API')
aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
region_name = "us-east-1"

# Set up Anthropic authentication

gateway.adapter.set_auth(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# Set the prompt for Agent with the necessary instructions
prompt = Prompt("You are a helpful assistant that can translate text and provide weather information. Use the relevant tools as needed, do not respond from memory. When the required answers are available, summarize the response and provide an answer.")
gateway.prepare_agent(prompt, tools=[translation_tool, weather_tool, ask_tool])

agent_input_1tool = "Translate 'Hello, how are you?' to German"
agent_input_2tools = "Translate 'Hello, how are you?' to Spanish and tell me the weather in Madrid"
agent_input_no_params = "Get me weather please"
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
#   gateway.start_conversation()
#    result_4 = gateway.run_agent(multiple_inputs)
#    print(f" Agent input: {multiple_inputs}, Agent output: {result_4}")
except Exception as e:
    print(str(e))

