import unittest
from unittest.mock import patch, MagicMock
from adapters.anthropic_claude_agent import AnthropicClaudeAgent
from core.response import Response, ResponseType
from core.abstract_tool import Tool

class TestAnthropicClaudeAgent(unittest.TestCase):

    def setUp(self):
        self.agent = AnthropicClaudeAgent("claude-2")

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
        self.assertEqual(self.agent.formatted_tools[0]["name"], "test_tool")

    def test_get_formatted_tool_output(self):
        formatted_output = self.agent.get_formatted_tool_output("tool_id", "Tool output")
        self.assertEqual(formatted_output, {
            "type": "tool_result",
            "tool_use_id": "tool_id",
            "content": "Tool output"
        })
