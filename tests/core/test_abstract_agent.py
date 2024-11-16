import unittest
from typing import Dict, Any
from agentgateway.core.abstract_agent import AbstractAgent
from agentgateway.core.response import Response, ResponseType
from agentgateway.core.abstract_tool import Tool

class ConcreteTool(Tool):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)

    def execute(self) -> Any:
        return "Tool executed"

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {}}

    def is_auth_setup(self) -> bool:
        return True

class ConcreteAgent(AbstractAgent):
    def run(self, agent_input, is_tool_response) -> Response:
        return Response(ResponseType.ANSWER, "Concrete agent response")

    def set_auth(self, **kwargs):
        self.auth_data.update(kwargs)

    def get_auth(self) -> Dict[str, Any]:
        return self.auth_data

    def set_model_config(self, **kwargs):
        self.model_config.update(kwargs)

    def get_model_config(self) -> Dict[str, Any]:
        return self.model_config

    def get_formatted_tool_output(self, tool, tool_output):
        return f"Tool {tool.name} output: {tool_output}"

class TestAbstractAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ConcreteAgent()

    def test_initialization(self):
        self.assertEqual(self.agent.instructions, "")
        self.assertEqual(self.agent.tools, {})
        self.assertEqual(self.agent.formatted_tools, [])
        self.assertEqual(self.agent.get_conversation_history(), [])
        self.assertEqual(self.agent.auth_data, {})
        self.assertEqual(self.agent.model_config, {"max_tokens": 2000, "temperature": 0.7})
        self.assertEqual(self.agent.model_id, "")

    def test_add_and_remove_tool(self):
        tool = ConcreteTool("test_tool", "A test tool")
        self.agent.add_tool(tool)
        self.assertEqual(len(self.agent.tools), 1)
        self.agent.remove_tool("test_tool")
        self.assertEqual(len(self.agent.tools), 0)

    def test_set_and_get_model(self):
        self.agent.set_model("gpt-4")
        self.assertEqual(self.agent.get_model(), "gpt-4")

    def test_set_instructions(self):
        instructions = "New instructions"
        self.agent.set_instructions(instructions)
        self.assertEqual(self.agent.instructions, instructions)

    def test_conversation_history(self):
        conversation_id = self.agent.start_conversation()
        self.agent.add_to_conversation_history({"role":"user", "content":"Hello"}, conversation_id)
        self.agent.add_to_conversation_history({"role":"assistant", "content":"Hi there"}, conversation_id)
        history = self.agent.get_conversation_history(conversation_id)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[1]["content"], "Hi there")

    def test_clear_conversation_history(self):
        self.agent.add_to_conversation_history("user", "Hello")
        self.agent.clear_conversation_history()
        self.assertEqual(len(self.agent.get_conversation_history()), 0)

    def test_get_formatted_conversation_history(self):
        conversation_id = self.agent.start_conversation()
        self.agent.add_to_conversation_history({"role": "user", "content": "Hello"}, conversation_id)
        self.agent.add_to_conversation_history({"role": "assistant", "content": "Hi there"}, conversation_id)

        formatted_history = self.agent.get_formatted_conversation_history(conversation_id)
        expected_history = "User: Hello\nAssistant: Hi there"
        self.assertEqual(formatted_history, expected_history)


    def test_run(self):
        response = self.agent.run("test input", False)
        self.assertEqual(response.response_type, ResponseType.ANSWER)
        self.assertEqual(response.content, "Concrete agent response")

    def test_set_and_get_auth(self):
        self.agent.set_auth(api_key="test_key")
        self.assertEqual(self.agent.get_auth(), {"api_key": "test_key"})

    def test_set_and_get_model_config(self):
        self.agent.set_model_config(max_tokens=1000)
        self.assertEqual(self.agent.get_model_config()["max_tokens"], 1000)

    def test_get_formatted_tool_output(self):
        tool = ConcreteTool("test_tool", "A test tool")
        formatted_output = self.agent.get_formatted_tool_output(tool, "Test output")
        self.assertEqual(formatted_output, "Tool test_tool output: Test output")

if __name__ == '__main__':
    unittest.main()