import pytest
from tools.tool_manager import ToolManager
from tools.askuser_tool import AskUserTool
from tools.weather_tool import WeatherTool
from tools.calculator_tool import CalculatorTool
from tools.translate_tool import TranslationTool


def test_tool_manager_get_tool():
    manager = ToolManager()

    ask_user_tool = manager.get_tool({"name": "ask_user", "input": {"question": "Test?"}, "id": "1"})
    assert isinstance(ask_user_tool, AskUserTool)

    weather_tool = manager.get_tool({"name": "get_weather", "input": {"location": "London,UK"}, "id": "2"})
    assert isinstance(weather_tool, WeatherTool)

    calculator_tool = manager.get_tool({"name": "calculate", "input": {"expression": "2+2"}, "id": "3"})
    assert isinstance(calculator_tool, CalculatorTool)

    translation_tool = manager.get_tool(
        {"name": "translate", "input": {"text": "Hello", "source_lang": "en", "target_lang": "es"}, "id": "4"})
    assert isinstance(translation_tool, TranslationTool)


def test_tool_manager_get_tool_unknown():
    manager = ToolManager()
    with pytest.raises(ValueError):
        manager.get_tool({"name": "unknown_tool", "input": {}, "id": "5"})


def test_tool_manager_validate_and_set_input():
    manager = ToolManager()
    calculator_tool = CalculatorTool()

    # Valid input
    manager._validate_and_set_input(calculator_tool, {"expression": "2+2"})
    assert calculator_tool.get_parameters()["expression"] == "2+2"

    # Missing required parameter
    with pytest.raises(ValueError):
        manager._validate_and_set_input(calculator_tool, {})

    # Invalid parameter type
    with pytest.raises(TypeError):
        manager._validate_and_set_input(calculator_tool, {"expression": 42})
