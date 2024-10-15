import unittest
from unittest.mock import patch, MagicMock
from adapters.bedrock_converse_agent import BedrockConverseAgent
from core.response import Response, ResponseType
from core.abstract_tool import Tool
import json

class TestBedrockConverseAgent(unittest.TestCase):

    def setUp(self):
        self.agent = BedrockConverseAgent("anthropic.claude-v2")

    def test_set_auth(self):
        self.agent.set_auth(
            aws_access_key_id="test_access_key",
            aws_secret_access_key="test_secret_key",
            region_name="us-west-2"
        )
        self.assertEqual(self.agent.auth_data["aws_access_key_id"], "test_access_key")
        self.assertEqual(self.agent.auth_data["aws_secret_access_key"], "test_secret_key")
        self.assertEqual(self.agent.auth_data["region_name"], "us-west-2")
        self.assertIsNotNone(self.agent.client)

    def test_set_auth_missing_key(self):
        with self.assertRaises(ValueError):
            self.agent.set_auth(aws_access_key_id="test_access_key")

    def test_set_model_config(self):
        self.agent.set_model_config(max_tokens=1000, temperature=0.5, top_p=0.9, stop_sequences=["END"])
        self.assertEqual(self.agent.model_config["max_tokens"], 1000)
        self.assertEqual(self.agent.model_config["temperature"], 0.5)
        self.assertEqual(self.agent.model_config["top_p"], 0.9)
        self.assertEqual(self.agent.model_config["stop_sequences"], ["END"])

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
        self.assertEqual(self.agent.formatted_tools[0]["toolSpec"]["name"], "test_tool")

    @patch('boto3.client')
    def test_run_answer(self, mock_boto3_client):
        self.agent.set_auth(
            aws_access_key_id="test_access_key",
            aws_secret_access_key="test_secret_key",
            region_name="us-west-2"
        )
        mock_response = {
            'output': {
                'message': {
                    'content': [{'text': 'Test response'}]
                }
            },
            'stopReason': 'stop'
        }
        mock_boto3_client.return_value.converse.return_value = mock_response

        response = self.agent.run("Test input", False)

        self.assertEqual(response.response_type, ResponseType.ANSWER)
        self.assertEqual(response.content, "Test response")

    def test_get_formatted_tool_output(self):
        mock_tool = MagicMock(spec=Tool)
        mock_tool.instance_id = "tool_id"
        formatted_output = self.agent.get_formatted_tool_output(mock_tool, "Tool output")
        self.assertEqual(formatted_output, {
            "toolResult": {
                "toolUseId": "tool_id",
                "content": [{"text": json.dumps("Tool output")}],
                "status": "success"
            }
        })
