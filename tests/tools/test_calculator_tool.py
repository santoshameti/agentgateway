import pytest
from agentgateway.tools.calculator_tool import CalculatorTool

def test_calculator_tool_initialization():
    tool = CalculatorTool()
    assert tool.name == "calculate"
    assert tool.description == "Perform basic arithmetic calculations"

def test_calculator_tool_is_auth_setup():
    tool = CalculatorTool()
    assert tool.is_auth_setup() == True

def test_calculator_tool_execute_valid():
    tool = CalculatorTool()
    tool.set_parameter("expression", "2 + 2")
    result = tool.execute()
    assert result == {"result": 4}

def test_calculator_tool_execute_invalid():
    tool = CalculatorTool()
    tool.set_parameter("expression", "2 + ")
    result = tool.execute()
    assert "error" in result

def test_calculator_tool_parameters_schema():
    tool = CalculatorTool()
    schema = tool.get_parameters_schema()
    assert schema["type"] == "object"
    assert "expression" in schema["properties"]
    assert "expression" in schema["required"]
