import json
import unittest
from unittest.mock import patch, MagicMock
from agentgateway.tools.sentiment_analysis_tool import SentimentAnalysisTool

class TestSentimentAnalysisTool(unittest.TestCase):
    def setUp(self):
        self.tool = SentimentAnalysisTool()
        self.tool.set_auth(api_key="dummy_key")

    @patch('agentgateway.tools.sentiment_analysis_tool.TextBlob')
    def test_sentiment_analysis(self, mock_textblob):
        # Mock the TextBlob object and its sentiment attribute
        mock_blob = MagicMock()
        mock_blob.sentiment.polarity = 0.8  # Set a mock polarity value for the test
        mock_textblob.return_value = mock_blob

        text = "I love this product! It's amazing and works perfectly."
        self.tool = SentimentAnalysisTool()  # Initialize the tool
        self.tool.set_parameters({"text": text})
        result = self.tool.execute()
        result = json.loads(result)

        # Assert the result contains expected keys and values
        self.assertIn("sentiment", result)
        self.assertIn("score", result)
        self.assertEqual(result["sentiment"], "positive")
        self.assertEqual(result["score"], 0.8)

        # Verify that TextBlob was called with the correct text
        mock_textblob.assert_called_once_with(text)

    def test_missing_api_key(self):
        self.tool.auth_data = {}  # Remove API key
        with self.assertRaises(ValueError):
            self.tool.execute()

if __name__ == '__main__':
    unittest.main()