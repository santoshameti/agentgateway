import unittest
from unittest.mock import patch, MagicMock
from agentgateway.adapters.fireworks_ai_agent import FireworksAIAgent
from agentgateway.core.response import Response, ResponseType
from agentgateway.core.abstract_tool import Tool
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function

class TestFireworksAIAgent(unittest.TestCase):

    def setUp(self):
        self.agent = FireworksAIAgent("accounts/fireworks/models/llama-v2-7b-chat")

    def test_set_auth(self):
        self.agent.set_auth(api_key="test_api_key")
        self.assertEqual(self.agent.auth_data, {"api_key": "test_api_key"})
        self.assertIsNotNone(self.agent.client)

    def test_set_auth_missing_key(self):
        with self.assertRaises(ValueError):
            self.agent.set_auth()

    def test_get_auth(self):
        self.agent.set_auth(api_key="test_api_key")
        self.assertEqual(self.agent.get_auth(), {"api_key": "test_api_key"})

    def test_set_model_config(self):
        self.agent.set_model_config(max_tokens=1000, temperature=0.5)
        self.assertEqual(self.agent.model_config["max_tokens"], 1000)
        self.assertEqual(self.agent.model_config["temperature"], 0.5)

    def test_set_model_config_invalid_key(self):
        with self.assertRaises(ValueError):
            self.agent.set_model_config(invalid_key=100)

    def test_get_model_config(self):
        self.agent.set_model_config(max_tokens=1000, temperature=0.5)
        config = self.agent.get_model_config()
        self.assertEqual(config["max_tokens"], 1000)
        self.assertEqual(config["temperature"], 0.5)

    def test_add_tool(self):
        mock_tool = MagicMock(spec=Tool)
        mock_tool.name = "test_tool"
        mock_tool.description = "A test tool"
        mock_tool.get_parameters_schema.return_value = {"properties": {}, "required": []}

        self.agent.add_tool(mock_tool)

        self.assertEqual(len(self.agent.formatted_tools), 1)
        self.assertEqual(self.agent.formatted_tools[0]["function"]["name"], "test_tool")
        self.assertEqual(len(self.agent.tools), 1)

    @patch('openai.OpenAI')
    def test_run_answer(self, mock_openai):
        self.agent.set_auth(api_key="test_api_key")
        mock_response = MagicMock()
        mock_response.choices[0].message = ChatCompletionMessage(role="assistant", content="Test response")
        mock_response.choices[0].finish_reason = "stop"
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        response = self.agent.run("Test input")

        self.assertEqual(response.response_type, ResponseType.ANSWER)
        self.assertEqual(response.content, "Test response")

    @patch('openai.OpenAI')
    def test_run_tool_call(self, mock_openai):
        self.agent.set_auth(api_key="test_api_key")
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
        mock_response = MagicMock()
        mock_response.choices[0].message = mock_message
        mock_response.choices[0].finish_reason = "tool_calls"
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        with patch('agentgateway.tools.tool_manager.ToolManager.get_tool') as mock_get_tool:
            mock_tool = MagicMock(spec=Tool)
            mock_get_tool.return_value = mock_tool
            response = self.agent.run("Test input")

        self.assertEqual(response.response_type, ResponseType.TOOL_CALL)
        self.assertEqual(len(response.tools), 1)

    def test_get_formatted_tool_output(self):
        mock_tool = MagicMock(spec=Tool)
        mock_tool.instance_id = "tool_id"
        mock_tool.name = "test_tool"
        formatted_output = self.agent.get_formatted_tool_output(mock_tool, "Tool output")
        self.assertEqual(formatted_output, {
            "tool_call_id": "tool_id",
            "role": "tool",
            "name": "test_tool",
            "content": "Tool output",
        })

    def test_run_without_auth(self):
        with self.assertRaises(ValueError):
            self.agent.run("Test input")

    @patch('openai.OpenAI')
    def test_run_with_exception(self, mock_openai):
        self.agent.set_auth(api_key="test_api_key")
        mock_openai.return_value.chat.completions.create.side_effect = Exception("API Error")

        response = self.agent.run("Test input")

        self.assertEqual(response.response_type, ResponseType.ERROR)
        self.assertEqual(response.content, "API Error")

if __name__ == '__main__':
    unittest.main()