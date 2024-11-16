import json
from typing import List, Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError

from agentgateway.core.abstract_agent import AbstractAgent
from agentgateway.core.abstract_tool import Tool
from agentgateway.core.response import Response, ResponseType
from agentgateway.utils.agent_logger import AgentLogger

class BedrockConverseAgent(AbstractAgent):
    def __init__(self, model_id: str):
        super().__init__(model_id)
        self.client = None
        self.formatted_tools = []
        self.logging = AgentLogger("BedrockConverseAgent")

    def set_auth(self, **kwargs):
        """
        Set the authentication data for Bedrock runtime.
        :param kwargs: Key-value pairs of authentication data.
        """
        required_params = ['aws_access_key_id', 'aws_secret_access_key', 'region_name']
        for param in required_params:
            if param not in kwargs:
                raise ValueError(f"Missing required authentication parameter: {param}")

        self.auth_data = {
            'aws_access_key_id': kwargs['aws_access_key_id'],
            'aws_secret_access_key': kwargs['aws_secret_access_key'],
            'region_name': kwargs['region_name']
        }
        self.client = boto3.client('bedrock-runtime', **self.auth_data)

    def get_auth(self) -> Dict[str, Any]:
        """
        Get the current authentication data.
        :return: A dictionary containing the current authentication data.
        """
        return {k: '********' if k.endswith('key') else v for k, v in self.auth_data.items()}

    def set_model_config(self, **kwargs):
        """
        Set or update the model configuration.
        :param kwargs: Key-value pairs of model configuration.
        """
        valid_keys = ['max_tokens', 'temperature', 'top_p', 'stop_sequences']
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
        Add a new tool to the agent's toolkit and format it for Bedrock Converse.
        :param tool: A Tool instance to be added.
        """
        formatted_tool = {
            "toolSpec": {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": {
                    "json": tool.get_parameters_schema()
                }
            }
        }
        self.formatted_tools.append(formatted_tool)
        self.tools[tool.name] = tool

    def run(self, agent_input, is_tool_response: Optional[bool] = False, conversation_id: Optional[str] = None) -> Response:
        self.logging.info("BedrockConverseAgent:run:Running Bedrock Converse Agent")

        if conversation_id is None:
            if self.current_conversation_id is None:
                raise ValueError("No conversation id provided. Please start conversation to get started.")
            else:
                conversation_id = self.current_conversation_id

        if not self.client:
            raise ValueError("Authentication not set. Please call set_auth() before running the agent.")

        response = Response()
        response.set_conversation_id(conversation_id)

        try:
            if not is_tool_response:
                self.add_to_conversation_history({"role":"user","content": [{"text": agent_input}]}, conversation_id)
            else:
                self.add_to_conversation_history({"role":"user", "content":agent_input}, conversation_id)

            body = {
                "modelId": self.model_id,
                "system" : [{"text": self.instructions}],
                "messages": self.get_conversation_history(conversation_id),
                "toolConfig": {
                    "tools": self.formatted_tools,
                },
                "inferenceConfig": {
                    "maxTokens": self.model_config.get('max_tokens', 2000),
                    "temperature": self.model_config.get('temperature', 0.7),
                    "topP": self.model_config.get('top_p', 1),
                    "stopSequences": self.model_config.get('stop_sequences', [])
                }
            }

            bedrock_response = self.client.converse(**body)

            assistant_message = bedrock_response['output']['message']['content']
            self.add_to_conversation_history({"role":"assistant", "content":assistant_message}, conversation_id)

            if bedrock_response['stopReason'] == "tool_use":
                self.logging.info("BedrockConverseAgent:run: tool use detected")
                response.set_response_type(ResponseType.TOOL_CALL)
                tools = self.get_tools(bedrock_response['output']['message'])
                response.set_tools(tools)
                self.logging.info("BedrockConverseAgent:run: tools extracted")
            else:
                response.set_response_type(ResponseType.ANSWER)
                response.set_content(assistant_message[0]['text'])

        except ClientError as e:
            response.set_response_type(ResponseType.ERROR)
            response.set_content(f"AWS Bedrock ClientError: {str(e)}")
        except Exception as e:
            response.set_response_type(ResponseType.ERROR)
            response.set_content(str(e))

        return response

    def get_tools(self, model_response) -> List[Tool]:
        self.logging.info("BedrockConverseAgent:get_tools: function called")
        tools = []
        # The model's response can consist of multiple content blocks
        for content_block in model_response["content"]:
            if "toolUse" in content_block:
                tool_use = content_block["toolUse"]
                tool_info = {
                    'name': tool_use['name'],
                    'input': tool_use['input'],
                    'id': tool_use['toolUseId']
                }
                self.logging.info(f"BedrockConverseAgent:get_tools: tool instance 'name': {tool_info['name']} 'input': {tool_info['input']}")
                tool = self.get_tool_from_response(tool_info)
                self.logging.info(f"BedrockConverseAgent:get_tools: tool instance 'name': {tool_info['name']} created")
                tools.append(tool)

        self.logging.info("BedrockConverseAgent:get_tools: compiled the tools and returning")
        return tools

    def get_formatted_tool_output(self, tool, tool_output):
        return {
                "toolResult": {
                    "toolUseId": tool.instance_id,
                    "content": [{"text": json.dumps(tool_output)}],
                    "status": "success"
                }
        }
