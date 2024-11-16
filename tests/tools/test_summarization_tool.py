import unittest
from unittest.mock import patch, MagicMock
from agentgateway.tools.text_summarization_tool import TextSummarizationTool

class TestTextSummarizationTool(unittest.TestCase):
    def setUp(self):
        self.tool = TextSummarizationTool()
        self.tool.set_auth(api_key="dummy_key")

    @patch('agentgateway.tools.text_summarization_tool.Anthropic')
    def test_summarization(self, mock_anthropic):
        # Mock the Anthropic client and its methods
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="This is a summary of the text.")]
        mock_client.messages.create.return_value = mock_response

        long_text = "This is a long text that needs to be summarized. " * 10
        self.tool.set_parameters({"text": long_text})
        summary = self.tool.execute()

        self.assertIsInstance(summary, str)
        self.assertEqual(summary, "This is a summary of the text.")
        mock_client.messages.create.assert_called_once()

    def test_missing_api_key(self):
        self.tool.auth_data = {}  # Remove API key
        with self.assertRaises(ValueError):
            self.tool.execute()

if __name__ == '__main__':
    unittest.main()