import json
import unittest
from tools.web_search_tool import WebSearchTool
from unittest.mock import patch, MagicMock

class TestWebSearchTool(unittest.TestCase):
    def setUp(self):
        self.tool = WebSearchTool()

    @patch('tools.web_search_tool.requests.get')
    def test_web_search(self, mock_get):
        # Mock the response
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <body>
                <div class="g">
                    <div class="r"><h3>Test Title 1</h3></div>
                    <div class="s">Test Snippet 1</div>
                    <a href="http://test1.com">Link 1</a>
                </div>
                <div class="g">
                    <div class="r"><h3>Test Title 2</h3></div>
                    <div class="s">Test Snippet 2</div>
                    <a href="http://test2.com">Link 2</a>
                </div>
            </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        self.tool.set_parameters({"query": "test query", "num_results": 2})
        results = json.loads(self.tool.execute())

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        self.assertIn("title", results[0])
        self.assertIn("link", results[0])
        self.assertIn("snippet", results[0])
        self.assertEqual(results[0]["link"], "http://test1.com")
        self.assertEqual(results[0]["snippet"], "Test Snippet 1")

if __name__ == '__main__':
    unittest.main()