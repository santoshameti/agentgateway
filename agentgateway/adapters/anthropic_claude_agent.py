import anthropic
import json
from typing import List, Dict, Any, Type, Optional
from agentgateway.core.abstract_agent import AbstractAgent
from agentgateway.core.abstract_tool import Tool
from agentgateway.core.response import Response, ResponseType
from anthropic.types import ToolUseBlock, TextBlock
from agentgateway.utils.agent_logger import AgentLogger


class AnthropicClaudeAgent(AbstractAgent):
    def __init__(self, model_id: str):
        super().__init__(model_id)
        self.client = None
        self.formatted_tools = []
        self.logging = AgentLogger("Agent")

    def set_auth(self, **kwargs):
        """
        Set the authentication data for Anthropic Claude.
        :param kwargs: Key-value pairs of authentication data.
        """
        if 'api_key' not in kwargs:
            raise ValueError("Missing required authentication parameter: api_key")

        self.auth_data = {'api_key': kwargs['api_key']}
        self.client = anthropic.Client(api_key=self.auth_data['api_key'])

    def get_auth(self) -> Dict[str, Any]:
        """
        Get the current authentication data.
        :return: A dictionary containing the current authentication data.
        """
        return self.auth_data  # Masked for security

    def set_model_config(self, **kwargs):
        """
        Set or update the model configuration.
        :param kwargs: Key-value pairs of model configuration.
        """
        valid_keys = ['max_tokens', 'temperature', 'model']
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
        Add a new tool to the agent's toolkit and format it for Claude.
        :param tool: A Tool instance to be added.
        """
        formatted_tool = {
            "name": tool.name,
            "description": tool.description,
            "input_schema": {
                "type": "object",
                "properties": tool.get_parameters_schema().get("properties", {}),
                "required": tool.get_parameters_schema().get("required", [])
            }
        }
        self.formatted_tools.append(formatted_tool)
        self.tools[tool.name] = tool

    def run(self, agent_input, is_tool_response: Optional[bool] = False, conversation_id: Optional[str] = None) -> Response:
        if conversation_id is None:
            if self.current_conversation_id is None:
                raise ValueError("No conversation id provided. Please start conversation to get started.")
            else:
                conversation_id = self.current_conversation_id

        self.logging.info("AnthropicClaudeAgent:run:Running Anthropic Claude Agent")
        if not self.client:
            raise ValueError("Authentication not set. Please call set_auth() before running the agent.")

        self.add_to_conversation_history({"role":"user", "content": agent_input}, conversation_id)

        response = Response()
        response.set_conversation_id(conversation_id)

        self.logging.info(f"AnthropicClaudeAgent:run:invoking the selected model {self.model_id}")
        try:
            if len(self.formatted_tools) > 0:
                model_response = self.client.messages.create(
                    model=self.model_id,
                    system=self.instructions,
                    max_tokens=self.model_config['max_tokens'],
                    temperature=self.model_config['temperature'],
                    messages=self.get_conversation_history(conversation_id),
                    tools=self.formatted_tools,
                    tool_choice={"type": "auto"}
                )
            else:
                model_response = self.client.messages.create(
                    model=self.model_id,
                    system=self.instructions,
                    max_tokens=self.model_config['max_tokens'],
                    temperature=self.model_config['temperature'],
                    messages=self.get_conversation_history(conversation_id)
                )

            self.logging.info(f"AnthropicClaudeAgent:run:model invoke completed")
            assistant_message = self.get_model_response(model_response.content)
            message = {"role":"assistant", "content":model_response.model_dump()}
            self.add_to_conversation_history(self.get_formatted_assistant_message(model_response.model_dump()), conversation_id)
            if model_response.stop_reason == "tool_use":
                self.logging.info(f"AnthropicClaudeAgent:run: tool use detected")
                response.set_response_type(ResponseType.TOOL_CALL)
                tools = self.get_tools(model_response.content)
                response.set_tools(tools)
                self.logging.info(f"AnthropicClaudeAgent:run: tools extracted")
            elif model_response.stop_reason == "end_turn":
                response.set_response_type(ResponseType.ANSWER)
                response.set_content(assistant_message)
            elif model_response.stop_reason == "max_tokens":
                response.set_response_type(ResponseType.ERROR)
                response.set_content(assistant_message)
        except Exception as e:
            response.set_response_type(ResponseType.ERROR)
            response.set_content(str(e))

        return response

    def get_formatted_tool_output(self, tool, tool_output):
        return {"type": "tool_result", "tool_use_id": tool.instance_id, "content": tool_output}


    def get_formatted_assistant_message(self, model_dump):
        # Extract text content from the content list
        text_contents = [
            item
            for item in model_dump.get('content', [])
            if item['type'] == 'text'
        ]

        tool_uses = [
            item for item in model_dump.get('content', [])
            if item['type'] == 'tool_use'
        ]

        text_contents = text_contents + tool_uses

        # Construct the message
        message = {
            "role": model_dump.get('role', 'assistant'),
            "content": text_contents
        }

        return message

    def get_tools(self, response) -> []:
        self.logging.info(f"AnthropicClaudeAgent:get_tools: function called")
        tools = []
        for item in response:
            if isinstance(item, ToolUseBlock):
                self.logging.info(f"AnthropicClaudeAgent:get_tools: tool instance 'name': {item.name} 'input': {item.input}")
                tool_info = {'name': item.name, 'input': item.input, 'id': item.id}
                tool = self.get_tool_from_response(tool_info)
                self.logging.info(f"AnthropicClaudeAgent:get_tools: tool instance 'name': {item.name} created")
                tools.append(tool)
                self.logging.info(f"AnthropicClaudeAgent:get_tools: compiled the tools and returning")
        return tools

    def get_model_response(self, response) -> str:
        for item in response:
            if isinstance(item, TextBlock):
                return item.text
        return ""
