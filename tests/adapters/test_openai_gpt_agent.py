import unittest
from unittest.mock import patch, MagicMock
from adapters.openai_gpt_agent import  OpenAIGPTAgent
from core.response import Response, ResponseType
from core.abstract_tool import Tool
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function

class TestOpenAIGPTAgent(unittest.TestCase):

    def setUp(self):
        self.agent = OpenAIGPTAgent("gpt-3.5-turbo")

    def test_set_auth(self):
        self.agent.set_auth(api_key="test_api_key")
        self.assertEqual(self.agent.auth_data, {"api_key": "test_api_key"})
        self.assertIsNotNone(self.agent.client)

    def test_set_auth_missing_key(self):
        with self.assertRaises(ValueError):
            self.agent.set_auth()

    def test_set_model_config(self):
        self.agent.set_model_config(max_tokens=1000, temperature=0.5)
        self.assertEqual(self.agent.model_config["max_tokens"], 1000)
        self.assertEqual(self.agent.model_config["temperature"], 0.5)

    def test_set_model_config_invalid_key(self):
        with self.assertRaises(ValueError):
            self.agent.set_model_config(invalid_key=100)

    def test_add_tool(self):
        mock_tool = MagicMock(spec=Tool)
        mock_tool.name = "test_tool"
        mock_tool.description = "A test tool"
        mock_tool.get_parameters_schema.return_value = {"properties": {}, "required": []}

        self.agent.add_tool(mock_tool)

        self.assertEqual(len(self.agent.formatted_tools), 1)
        self.assertEqual(self.agent.formatted_tools[0]["function"]["name"], "test_tool")

    def test_get_formatted_tool_output(self):
        mock_tool = MagicMock(spec=Tool)
        mock_tool.instance_id = "tool_id"
        formatted_output = self.agent.get_formatted_tool_output(mock_tool, "Tool output")
        self.assertEqual(formatted_output, {
            "role": "tool",
            "tool_call_id": "tool_id",
            "content": '"Tool output"'
        })

    def test_generate_assistant_message_for_toolcalls(self):
        mock_function = Function(name="test_tool", arguments='{"param": "value"}')
        mock_tool_call = ChatCompletionMessageToolCall(
            id="tool_id",
            type="function",
            function=mock_function
        )
        mock_message = ChatCompletionMessage(
            role="assistant",
            content=None,
            tool_calls=[mock_tool_call]
        )

        assistant_message = self.agent.generate_assistant_message_for_toolcalls(mock_message)

        self.assertEqual(assistant_message["role"], "assistant")
        self.assertEqual(len(assistant_message["tool_calls"]), 1)
        self.assertEqual(assistant_message["tool_calls"][0]["function"]["name"], "test_tool")
