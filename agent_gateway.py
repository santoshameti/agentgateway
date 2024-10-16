from typing import Union, List
from enum import Enum
from core.abstract_agent import AbstractAgent
from core.prompt import Prompt
from core.abstract_tool import Tool
from core.response import Response, ResponseType
from utils.agent_logger import AgentLogger
from adapters.anthropic_claude_agent import AnthropicClaudeAgent
from adapters.openai_gpt_agent import OpenAIGPTAgent
from adapters.bedrock_converse_agent import BedrockConverseAgent
from adapters.groq_agent import GroqAgent
from adapters.together_ai_agent import TogetherAIAgent

class AgentType(Enum):
    BEDROCK = "bedrock"
    OPENAI = "openai"
    VERTEX = "vertex"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    TOGETHER = "together"

class UnsupportedAgentException(Exception):
    def __init__(self, agent_type):
        self.agent_type = agent_type
        super().__init__(f"Unsupported agent type: {agent_type}")

class AgentGateway:
    def __init__(self, agent_type_or_adapter: Union[AgentType, AbstractAgent], model_id):
        self.logging = AgentLogger("Agent")
        self.tools = {}
        if isinstance(agent_type_or_adapter, AgentType):
            self.agent_type = agent_type_or_adapter
            self.adapter = self._get_adapter(agent_type_or_adapter, model_id)
        elif isinstance(agent_type_or_adapter, AbstractAgent):
            self.agent_type = None
            self.adapter = agent_type_or_adapter
        else:
            raise UnsupportedAgentException(type(agent_type_or_adapter).__name__)

    def _get_adapter(self, agent_type: AgentType, model_id) -> AbstractAgent:
        self.logging.info(f"AgentGateway:_get_adapter:Fetching adapter for {agent_type}")
        if agent_type == AgentType.BEDROCK:
            self.adapter = BedrockConverseAgent(model_id)
            return self.adapter
        elif agent_type == AgentType.OPENAI:
            self.adapter = OpenAIGPTAgent(model_id)
            return self.adapter
        elif agent_type == AgentType.ANTHROPIC:
            self.adapter = AnthropicClaudeAgent(model_id)
            return self.adapter
        elif agent_type == AgentType.GROQ:
            self.adapter = GroqAgent(model_id)
            return self.adapter
        elif agent_type == AgentType.TOGETHER:
            self.adapter = TogetherAIAgent(model_id)
            return self.adapter
        elif agent_type == AgentType.VERTEX:
            pass
        else:
            raise UnsupportedAgentException(agent_type.value)

    def prepare_agent(self, prompt: Prompt, tools: list[Tool] = []):
        self.logging.info(f"AgentGateway:create_agent: Preparing the requested agent")
        self.adapter.set_instructions(prompt.content)

        for tool in tools:
            self.logging.info(f"AgentGateway:create_agent: Iterating the tools and validating auth {tool.is_auth_setup()}")
            if tool.is_auth_setup():
                self.adapter.add_tool(tool)
                self.tools[tool.name] = tool
            else:
                self.logging.info(
                    f"AgentGateway:create_agent: Tools {tool.name} auth is not setup, exiting")
                raise ValueError(f"Invalid auth setup: {tool.name}")

    def run_agent(self, agent_input):
        final_answer = False
        tool_response = False
        self.logging.info(f"AgentGateway:run_agent:Running agent for {agent_input}")
        while not final_answer:

            response = self.adapter.run(agent_input, is_tool_response=tool_response)
            self.logging.info(f"AgentGateway:run_agent:Agent execution completed")
            if response.response_type == ResponseType.ANSWER:
                self.logging.info(f"AgentGateway:run_agent:Final answer from Agent")
                final_answer = True
                tool_response = False
                return response.content
            elif response.response_type == ResponseType.TOOL_CALL:
                self.logging.info(f"AgentGateway:run_agent:Agent responds with tool use")
                tool_results = []
                response_tools = response.get_tools()
                self.logging.info(f"AgentGateway:run_agent: iterating tools")

                for response_tool in response_tools:
                    self.logging.info(f"AgentGateway:run_agent: executing tool {response_tool.name} and id {response_tool.instance_id}")
                    if response_tool.name in self.tools:
                        # get the auth and set the auth to execute
                        self.logging.info(f"AgentGateway:run_agent: setting the auth params for the agents to execute")
                        response_tool_name = response_tool.name
                        response_tool_auth = self.tools[response_tool_name].get_auth()
                        response_tool.set_auth(**response_tool_auth)
                        tool_output = response_tool.execute()
                        formatted_tool_output = self.adapter.get_formatted_tool_output(tool=response_tool,tool_output=tool_output)
                        tool_results.append(formatted_tool_output)
                        self.logging.info(f"AgentGateway:run_agent: {response_tool.get_name()} tool output: {tool_output}")
                    else:
                        self.logging.info(f"AgentGateway:run_agent: invalid tool {response_tool.get_name()} returned by Agent")
                        raise UnsupportedAgentException(f"{response_tool.get_name()} returned by Agent")
                    self.logging.info(f"AgentGateway:run_agent:Agent execution completed")

                agent_input=tool_results
                tool_response = True
            elif response.response_type == ResponseType.ERROR:
                self.logging.info(f"AgentGateway:run_agent:Agent Errored {response.content}")
                raise Exception(f"Agent encountered an error: {response.content}")