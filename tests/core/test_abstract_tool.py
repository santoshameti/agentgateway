import unittest
from typing import Dict, Any
from abc import ABC, abstractmethod
from agentgateway.core.abstract_tool import Tool

class ConcreteTool(Tool):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)

    def execute(self) -> Any:
        return "Executed"

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "param1": {"type": "string"},
                "param2": {"type": "integer"}
            },
            "required": ["param1"]
        }

    def is_auth_setup(self) -> bool:
        return bool(self.auth_data)

class TestAbstractTool(unittest.TestCase):
    def setUp(self):
        self.tool = ConcreteTool("TestTool", "A test tool")

    def test_initialization(self):
        self.assertEqual(self.tool.name, "TestTool")
        self.assertEqual(self.tool.description, "A test tool")
        self.assertEqual(self.tool.instance_id, "")
        self.assertEqual(self.tool.auth_data, {})
        self.assertEqual(self.tool._parameters, {})

    def test_to_dict(self):
        expected_dict = {
            "type": "function",
            "function": {
                "name": "TestTool",
                "description": "A test tool",
                "parameters": self.tool.get_parameters_schema()
            }
        }
        self.assertEqual(self.tool.to_dict(), expected_dict)

    def test_set_and_get_auth(self):
        self.tool.set_auth(api_key="test_key")
        self.assertEqual(self.tool.get_auth(), {"api_key": "test_key"})

    def test_is_auth_setup(self):
        self.assertFalse(self.tool.is_auth_setup())
        self.tool.set_auth(api_key="test_key")
        self.assertTrue(self.tool.is_auth_setup())

    def test_set_and_get_parameters(self):
        self.tool.set_parameters({"param1": "value1", "param2": 42})
        self.assertEqual(self.tool.get_parameters(), {"param1": "value1", "param2": 42})

    def test_set_invalid_parameter(self):
        with self.assertRaises(ValueError):
            self.tool.set_parameters({"invalid_param": "value"})

    def test_set_missing_required_parameter(self):
        with self.assertRaises(ValueError):
            self.tool.set_parameters({"param2": 42})

    def test_get_parameter(self):
        self.tool.set_parameters({"param1": "value1", "param2": 42})
        self.assertEqual(self.tool.get_parameter("param1"), "value1")
        self.assertEqual(self.tool.get_parameter("param2"), 42)

    def test_get_nonexistent_parameter(self):
            self.assertEqual(self.tool.get_parameter("nonexistent"), None)

    def test_set_and_get_instance_id(self):
        self.tool.set_instance_id("instance_1")
        self.assertEqual(self.tool.get_instance_id(), "instance_1")

    def test_get_name(self):
        self.assertEqual(self.tool.get_name(), "TestTool")

    def test_clone(self):
        self.tool.set_parameters({"param1": "value1", "param2": 42})
        self.tool.set_auth(api_key="test_key")
        self.tool.set_instance_id("instance_1")

        cloned_tool = self.tool.clone()

        self.assertEqual(cloned_tool.name, self.tool.name)
        self.assertEqual(cloned_tool.description, self.tool.description)
        self.assertEqual(cloned_tool.get_parameters(), self.tool.get_parameters())
        self.assertEqual(cloned_tool.get_auth(), self.tool.get_auth())
        self.assertNotEqual(cloned_tool.get_instance_id(), self.tool.get_instance_id())
        self.assertEqual(cloned_tool.get_instance_id(), "")

    def test_execute(self):
        self.assertEqual(self.tool.execute(), "Executed")

if __name__ == '__main__':
    unittest.main()