import json
import unittest
from unittest.mock import patch, MagicMock
from agentgateway.tools.sentiment_analysis_tool import SentimentAnalysisTool

class TestSentimentAnalysisTool(unittest.TestCase):
    def setUp(self):
        self.tool = SentimentAnalysisTool()
        self.tool.set_auth(api_key="dummy_key")

    @patch('agentgateway.tools.sentiment_analysis_tool.Anthropic')
    def test_sentiment_analysis(self, mock_anthropic):
        # Mock the Anthropic client and its methods
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Sentiment: Positive\nScore: 0.8")]
        mock_client.messages.create.return_value = mock_response

        text = "I love this product! It's amazing and works perfectly."
        self.tool.set_parameters({"text": text})
        result = self.tool.execute()
        result = json.loads(result)

        self.assertIn("sentiment", result)
        self.assertIn("score", result)
        self.assertEqual(result["sentiment"], "positive")
        self.assertEqual(result["score"], 0.8)
        mock_client.messages.create.assert_called_once()

    def test_missing_api_key(self):
        self.tool.auth_data = {}  # Remove API key
        with self.assertRaises(ValueError):
            self.tool.execute()

if __name__ == '__main__':
    unittest.main()