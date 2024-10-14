import pytest
from tools.askuser_tool import AskUserTool
from unittest.mock import patch


def test_askuser_tool_initialization():
    tool = AskUserTool()
    assert tool.name == "ask_user"
    assert tool.description == "This tool is to get input from a user. Pick the tool to set the question to ask for user input"


def test_askuser_tool_is_auth_setup():
    tool = AskUserTool()
    assert tool.is_auth_setup() == True


def test_askuser_tool_execute():
    tool = AskUserTool()
    tool.set_parameter("question", "What is your name?")

    with patch('builtins.input', return_value="John Doe"):
        result = tool.execute()

    assert result == "John Doe"


def test_askuser_tool_parameters_schema():
    tool = AskUserTool()
    schema = tool.get_parameters_schema()
    assert schema["type"] == "object"
    assert "question" in schema["properties"]
    assert "question" in schema["required"]
