from openai import OpenAI, ChatCompletion
import json, traceback
from typing import List, Dict, Any, Optional
from openai.types.chat import ChatCompletionMessageToolCall
from agentgateway.core.abstract_agent import AbstractAgent
from agentgateway.core.abstract_tool import Tool
from agentgateway.core.response import Response, ResponseType
from agentgateway.utils.agent_logger import AgentLogger


class OpenAIGPTAgent(AbstractAgent):
    def __init__(self, model_id: str):
        super().__init__(model_id)
        self.client = None
        self.formatted_tools = []
        self.logging = AgentLogger("Agent")

    def set_auth(self, **kwargs):
        if 'api_key' not in kwargs:
            raise ValueError("Missing required authentication parameter: api_key")

        self.auth_data = {'api_key': kwargs['api_key']}
        self.client = OpenAI(api_key=self.auth_data['api_key'])

    def get_auth(self) -> Dict[str, Any]:
        return self.auth_data

    def set_model_config(self, **kwargs):
        valid_keys = ['max_tokens', 'temperature', 'model']
        for key, value in kwargs.items():
            if key in valid_keys:
                self.model_config[key] = value
            else:
                raise ValueError(f"Invalid configuration parameter: {key}")

    def get_model_config(self) -> Dict[str, Any]:
        return self.model_config.copy()

    def add_tool(self, tool: Tool):
        formatted_tool = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": tool.get_parameters_schema().get("properties", {}),
                    "required": tool.get_parameters_schema().get("required", [])
                }
            }
        }
        self.formatted_tools.append(formatted_tool)
        self.tools[tool.name] = tool

    def get_tools(self, response) -> List[Tool]:
        self.logging.info(f"OpenAIAgent:get_tools: function called")
        tools = []

        for item in response.tool_calls:
            if isinstance(item, ChatCompletionMessageToolCall):
                tool_input = item.function.arguments
                try:
                    tool_input = json.loads(tool_input)
                except (ValueError, TypeError):
                    pass  # tool_input is already a dictionary

                self.logging.info(f"OpenAIAgent:get_tools: tool instance 'name': {item.function.name} 'input': {tool_input}")
                tool_info = {'name': item.function.name, 'input': tool_input, 'id': item.id}

                tool = self.get_tool_from_response(tool_info)
                self.logging.info(f"OpenAIAgent:get_tools: tool instance 'name': {item.function.name} created")
                tools.append(tool)
                self.logging.info(f"OpenAIAgent:get_tools: compiled the tools and returning")

        self.logging.info(f"OpenAIAgent:get_tools: compiled the tools and returning")
        return tools

    def get_formatted_tool_output(self, tool, tool_output):
        return {"role": "tool", "tool_call_id": tool.instance_id, "content": json.dumps(tool_output)}

    def run(self, agent_input, is_tool_response: Optional[bool] = False, conversation_id: Optional[str] = None) -> Response:
        self.logging.info("OpenAIAgent:run:Running OpenAI Agent")

        if conversation_id is None:
            if self.current_conversation_id is None:
                raise ValueError("No conversation id provided. Please start conversation to get started.")
            else:
                conversation_id = self.current_conversation_id

        response = Response()
        response.set_conversation_id(conversation_id)

        if not self.client:
            raise ValueError("Authentication not set. Please call set_auth() before running the agent.")

        if not is_tool_response:
            self.add_to_conversation_history({"role":"user", "content":agent_input}, conversation_id)
        elif is_tool_response:
            self.extend_conversation_history(agent_input, conversation_id)

        messages = [
            {"role": "system", "content": self.instructions}
        ]
        messages.extend(self.get_conversation_history(conversation_id))

        self.logging.info(f"OpenAIAgent:run:invoking the selected model {self.model_id}")
        try:
            if len(self.tools) > 0:
                model_response = self.client.chat.completions.create(
                    model=self.model_id,
                    messages=messages,
                    max_tokens=self.model_config['max_tokens'],
                    temperature=self.model_config['temperature'],
                    tools=self.formatted_tools
                )
            else:
                model_response = self.client.chat.completions.create(
                    model=self.model_id,
                    messages=messages,
                    max_tokens=self.model_config['max_tokens'],
                    temperature=self.model_config['temperature']
                )

            self.logging.info(f"OpenAIAgent:run:model invoke completed")
            finish_reason = model_response.choices[0].finish_reason
            if finish_reason != "tool_calls":
                assistant_message = model_response.choices[0].message.content
                self.add_to_conversation_history({"role":"assistant", "content":assistant_message}, conversation_id)
            else:
                assistant_message = self.generate_assistant_message_for_toolcalls(model_response.choices[0].message )
                self.add_to_conversation_history(assistant_message, conversation_id)

            if finish_reason == "tool_calls":
                self.logging.info(f"OpenAIAgent:run: function call detected")
                response.set_response_type(ResponseType.TOOL_CALL)
                tools = self.get_tools(model_response.choices[0].message)

                response.set_tools(tools)
                self.logging.info(f"OpenAIAgent:run: tools extracted")

            elif finish_reason == "stop":
                response.set_response_type(ResponseType.ANSWER)
                response.set_content(assistant_message)
            elif finish_reason == "length":
                response.set_response_type(ResponseType.ERROR)
                response.set_content("Response exceeded maximum token limit.")
            elif finish_reason == "content_filter":
                response.set_response_type(ResponseType.ERROR)
                response.set_content("Response was filtered due to content safety.")
            else:
                response.set_response_type(ResponseType.ERROR)
                response.set_content(f"Unexpected finish reason: {finish_reason}")

        except Exception as e:
            response.set_response_type(ResponseType.ERROR)
            response.set_content(str(e))

        return response

    def generate_assistant_message_for_toolcalls(self, chat_message):
        """
            Takes a ChatCompletionMessage and generates an assistant message to append.

            Parameters:
            chat_message (dict): The input ChatCompletionMessage.

            Returns:
            dict: The assistant message formatted for appending.
            """
        # Extracting information from the input message
        role = chat_message.role
        tool_calls = chat_message.tool_calls

        # Create the assistant message structure
        assistant_message = {
            "role": role,
            "tool_calls": []
        }

        # Process tool calls if they exist
        for tool in tool_calls:
            # Create a structured tool call message
            tool_call_message = {
                "id": tool.id,
                "type": "function",
                "function": {
                    "name": tool.function.name,
                    "arguments": tool.function.arguments
                }
            }
            assistant_message["tool_calls"].append(tool_call_message)
        return assistant_message
