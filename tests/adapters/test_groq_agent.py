import unittest
from unittest.mock import patch, MagicMock
from groq.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
from agentgateway.core.response import Response, ResponseType
from agentgateway.core.abstract_tool import Tool
from agentgateway.adapters.groq_agent import GroqAgent

class TestGroqAgent(unittest.TestCase):

    def setUp(self):
        self.agent = GroqAgent("groq-model-id")

    def test_set_auth(self):
        self.agent.set_auth(api_key="test_api_key")
        self.assertEqual(self.agent.auth_data, {"api_key": "test_api_key"})
        self.assertIsNotNone(self.agent.client)

    def test_set_auth_missing_key(self):
        with self.assertRaises(ValueError):
            self.agent.set_auth()

    def test_get_auth(self):
        self.agent.set_auth(api_key="test_api_key")
        auth_data = self.agent.get_auth()
        self.assertEqual(auth_data, {"api_key": "test_api_key"})

    def test_set_model_config(self):
        self.agent.set_model_config(max_tokens=100, temperature=0.7)
        self.assertEqual(self.agent.model_config["max_tokens"], 100)
        self.assertEqual(self.agent.model_config["temperature"], 0.7)

    def test_set_model_config_invalid_param(self):
        with self.assertRaises(ValueError):
            self.agent.set_model_config(invalid_param=1)

    def test_get_model_config(self):
        self.agent.set_model_config(max_tokens=100, temperature=0.7)
        config = self.agent.get_model_config()
        self.assertEqual(config["max_tokens"], 100)
        self.assertEqual(config["temperature"], 0.7)

    def test_add_tool(self):
        mock_tool = MagicMock(spec=Tool)
        mock_tool.name = "test_tool"
        mock_tool.description = "A test tool"
        mock_tool.get_parameters_schema.return_value = {"type": "object", "properties": {}}

        self.agent.add_tool(mock_tool)

        self.assertEqual(len(self.agent.formatted_tools), 1)
        self.assertEqual(len(self.agent.tools), 1)
        self.assertEqual(self.agent.formatted_tools[0]["function"]["name"], "test_tool")

    @patch("groq.Client")
    def test_run_answer(self, mock_client):
        self.agent.set_auth(api_key="test_api_key")
        mock_response = MagicMock()
        mock_response.choices[0].finish_reason = "stop"
        mock_response.choices[0].message = ChatCompletionMessage(role="assistant", content="Test answer")
        mock_client.return_value.chat.completions.create.return_value = mock_response

        response = self.agent.run("Test input", is_tool_response=False)

        self.assertEqual(response.response_type, ResponseType.ANSWER)
        self.assertEqual(response.content, "Test answer")

    def test_get_formatted_tool_output(self):
        mock_tool = MagicMock(spec=Tool)
        mock_tool.instance_id = "test_id"
        mock_tool.name = "test_tool"

        formatted_output = self.agent.get_formatted_tool_output(mock_tool, "Tool output")

        self.assertEqual(formatted_output["tool_call_id"], "test_id")
        self.assertEqual(formatted_output["role"], "tool")
        self.assertEqual(formatted_output["name"], "test_tool")
        self.assertEqual(formatted_output["content"], "Tool output")

if __name__ == '__main__':
    unittest.main()