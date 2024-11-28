import unittest
from agentgateway.core.response import Response, ResponseType

class TestResponse(unittest.TestCase):
    def setUp(self):
        self.response = Response()

    def test_initialization(self):
        self.assertIsNone(self.response.response_type)
        self.assertIsNone(self.response.content)
        self.assertIsNone(self.response.conversation_id)
        self.assertEqual(self.response.tools, [])

    def test_set_response_type(self):
        self.response.set_response_type(ResponseType.ANSWER)
        self.assertEqual(self.response.response_type, ResponseType.ANSWER)

    def test_set_content(self):
        content = "Test content"
        self.response.set_content(content)
        self.assertEqual(self.response.content, content)

    def test_set_tools(self):
        tools = ["tool1", "tool2"]
        self.response.set_tools(tools)
        self.assertEqual(self.response.get_tools(), tools)

    def test_set_and_get_conversation_id(self):
        conversation_id = "test_conversation"
        self.response.set_conversation_id(conversation_id)
        self.assertEqual(self.response.get_conversation_id(), conversation_id)

    def test_to_dict(self):
        self.response.set_response_type(ResponseType.TOOL_CALL)
        self.response.set_content("Use tool X")
        self.response.set_tools(["tool1"])
        self.response.set_conversation_id("test_conversation")
        expected_dict = {
            "type": "tool_use",
            "content": "Use tool X",
            "tools": ["tool1"],
            "conversation_id": "test_conversation",
            "llm_usage": {'llm_calls':0, 'total_input_tokens':0, 'total_output_tokens':0}
        }
        self.assertEqual(self.response.to_dict(), expected_dict)

    def test_str_representation(self):
        self.response.set_response_type(ResponseType.ASK_USER)
        self.response.set_content("What's your name?")
        self.response.set_conversation_id("test_conversation")
        self.assertEqual(self.response.content, "What's your name?")
        self.assertEqual(self.response.conversation_id, "test_conversation")


if __name__ == '__main__':
    unittest.main()