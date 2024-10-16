import os
from dotenv import load_dotenv
from agent_gateway import AgentGateway, AgentType
from core.prompt import Prompt
from tools.weather_tool import WeatherTool
from tools.translate_tool import TranslationTool
from tools.askuser_tool import AskUserTool
from tools.web_search_tool import WebSearchTool

# Load environment variables
load_dotenv()

# create the tools needed for the agent
translation_tool = TranslationTool()
weather_tool = WeatherTool()
ask_tool = AskUserTool()
search_tool = WebSearchTool()

# Set up tool authentication from the .env files
translation_tool.set_auth(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Create the agent gateway
gateway = AgentGateway(AgentType.ANTHROPIC, model_id="claude-3-5-sonnet-20240620")

# Set up Anthropic authentication
gateway.adapter.set_auth(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Set the prompt for Agent with the necessary instructions
prompt = Prompt("You are a helpful assistant that has access to tools like translation, web search, weather. When asked about current affairs, please use webs search tool. Use the relevant tools as needed, do not respond from memory. When the required answers are available, summarize the response and provide an answer.")
gateway.prepare_agent(prompt, tools=[search_tool, translation_tool, weather_tool, ask_tool])

agent_input_1tool = "What is the latest status from the US election primaries debate"


try:
    result_1 = gateway.run_agent(agent_input_1tool)
    print(result_1)
#    result_2 = gateway.run_agent(agent_input_2tools)
#    print(result_2)
#    result_3 = gateway.run_agent(agent_input_no_params)
#    print(result_3)
except Exception as e:
    print(str(e))

