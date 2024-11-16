import json
from typing import List, Dict, Any, Optional

import openai
from openai.types.chat import ChatCompletionMessageToolCall
from agentgateway.core.abstract_agent import AbstractAgent
from agentgateway.core.abstract_tool import Tool
from agentgateway.core.response import Response, ResponseType
from agentgateway.utils.agent_logger import AgentLogger

class FireworksAIAgent(AbstractAgent):
    def __init__(self, model_id: str):
        super().__init__(model_id)
        self.api_url = "https://api.fireworks.ai/inference/v1"
        self.formatted_tools = []
        self.logging = AgentLogger("Agent")

    def set_auth(self, **kwargs):
        """
        Set the authentication data for Fireworks AI API.
        :param kwargs: Key-value pairs of authentication data.
        """
        if 'api_key' not in kwargs:
            raise ValueError("Missing required authentication parameter: api_key")

        self.auth_data = {
            'api_key': kwargs['api_key']
        }
        self.client = openai.OpenAI(base_url=self.api_url, api_key=kwargs['api_key'])

    def get_auth(self) -> Dict[str, Any]:
        """
        Get the current authentication data.
        :return: A dictionary containing the current authentication data.
        """
        return self.auth_data

    def set_model_config(self, **kwargs):
        """
        Set or update the model configuration.
        :param kwargs: Key-value pairs of model configuration.
        """
        valid_keys = ['max_tokens', 'temperature', 'top_p', 'stop']
        for key, value in kwargs.items():
            if key in valid_keys:
                self.model_config[key] = value
            else:
                raise ValueError(f"Invalid configuration parameter: {key}")

    def get_model_config(self) -> Dict[str, Any]:
        """
        Get the current model configuration.
        :return: A dictionary containing the current model configuration.
        """
        return self.model_config.copy()

    def add_tool(self, tool: Tool):
        """
        Add a new tool to the agent's toolkit and format it for Fireworks AI.
        :param tool: A Tool instance to be added.
        """
        formatted_tool = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.get_parameters_schema()
            }
        }
        self.formatted_tools.append(formatted_tool)
        self.tools[tool.name] = tool

    def run(self, agent_input, is_tool_response: Optional[bool] = False, conversation_id: Optional[str] = None) -> Response:
        self.logging.info("FireworksAIAgent:run:Running Fireworks AI Agent")
        if not self.auth_data:
            raise ValueError("Authentication not set. Please call set_auth() before running the agent.")

        if conversation_id is None:
            if self.current_conversation_id is None:
                raise ValueError("No conversation id provided. Please start conversation to get started.")
            else:
                conversation_id = self.current_conversation_id

        response = Response()
        response.set_conversation_id(conversation_id)

        try:
            if not is_tool_response:
                self.add_to_conversation_history({"role":"user", "content":agent_input},conversation_id)
            else:
                self.extend_conversation_history(agent_input, conversation_id)

            messages = [
                {"role": "system", "content": self.instructions}
            ]
            messages.extend(self.get_conversation_history(conversation_id))

            fireworks_response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                tools=self.formatted_tools,
                tool_choice="auto",
                **self.model_config
            )

            assistant_message = fireworks_response.choices[0].message
            self.add_to_conversation_history(assistant_message, conversation_id)
            finish_reason = fireworks_response.choices[0].finish_reason

            if finish_reason == "tool_calls":
                self.logging.info("FireworksAIAgent:run: function call detected")
                response.set_response_type(ResponseType.TOOL_CALL)
                tools = self.get_tools(assistant_message.tool_calls)
                response.set_tools(tools)
                self.logging.info("FireworksAIAgent:run: tools extracted")
            else:
                response.set_response_type(ResponseType.ANSWER)
                response.set_content(assistant_message.content)

        except Exception as e:
            response.set_response_type(ResponseType.ERROR)
            response.set_content(str(e))

        return response

    def get_tools(self, tool_calls) -> List[Tool]:
        self.logging.info("FireworksAIAgent:get_tools: function called")
        tools = []

        for item in tool_calls:
            if isinstance(item, ChatCompletionMessageToolCall):
                tool_input = item.function.arguments
                try:
                    tool_input = json.loads(tool_input)
                except (ValueError, TypeError):
                    pass  # tool_input is already a dictionary

                self.logging.info(f"FireworksAIAgent:get_tools: tool instance 'name': {item.function.name} 'input': {tool_input}")
                tool_info = {'name': item.function.name, 'input': tool_input, 'id': item.id}

                tool = self.get_tool_from_response(tool_info)
                self.logging.info(f"FireworksAIAgent:get_tools: tool instance 'name': {item.function.name} created")
                tools.append(tool)

        self.logging.info(f"FireworksAIAgent:get_tools: compiled the tools and returning")
        return tools

    def get_formatted_tool_output(self, tool, tool_output):
        return {
            "tool_call_id": tool.instance_id,
            "role": "tool",
            "name": tool.name,
            "content": tool_output,
        }