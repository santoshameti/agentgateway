import json
import unittest
from unittest.mock import patch, MagicMock
from tools.topic_detection_tool import TopicDetectionTool


class TestTopicDetectionTool(unittest.TestCase):
    def setUp(self):
        self.tool = TopicDetectionTool()
        self.tool.set_auth(api_key="dummy_key")

    @patch('tools.topic_detection_tool.Anthropic')
    def test_topic_detection(self, mock_anthropic):
        # Mock the Anthropic client and its methods
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="""
        1. Artificial Intelligence: AI, machine learning, intelligence
        2. Natural Language Processing: NLP, language, processing
        3. Computer Science: algorithms, computation, programming
        """)]
        mock_client.messages.create.return_value = mock_response

        text = """
        Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.

        Machine learning (ML) is a field of inquiry devoted to understanding and building methods that 'learn', that is, methods that leverage data to improve performance on some set of tasks. It is seen as a part of artificial intelligence.

        Natural Language Processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data.
        """

        self.tool.set_parameters({"text": text})
        results = json.loads(self.tool.execute())

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 3)  # We mocked 3 topics
        self.assertIn("label", results[0])
        self.assertIn("words", results[0])

        # Check if some expected words are in the topics
        all_words = ' '.join([' '.join(item['words']) for item in results]).lower()
        expected_words = ['intelligence', 'ai', 'learning', 'language']
        for word in expected_words:
            self.assertIn(word, all_words)

        mock_client.messages.create.assert_called_once()

    def test_missing_api_key(self):
        self.tool.auth_data = {}  # Remove API key
        with self.assertRaises(ValueError):
            self.tool.execute()


if __name__ == '__main__':
    unittest.main()