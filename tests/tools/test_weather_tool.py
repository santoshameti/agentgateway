import pytest
from tools.weather_tool import WeatherTool
from unittest.mock import patch, MagicMock


def test_weather_tool_initialization():
    tool = WeatherTool()
    assert tool.name == "get_weather"
    assert tool.description == "Get the current weather for a specified location"


def test_weather_tool_is_auth_setup():
    tool = WeatherTool()
    assert tool.is_auth_setup() == True


@patch('tools.weather_tool.requests.get')
@patch('tools.weather_tool.WeatherTool.get_coordinates')
def test_weather_tool_execute(mock_get_coordinates, mock_requests_get):
    tool = WeatherTool()
    tool.set_parameter("location", "London,UK")

    mock_get_coordinates.return_value = (51.5074, -0.1278)

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "hourly": {"temperature_2m": [20], "precipitation": [0], "windspeed_10m": [10]},
        "daily": {"temperature_2m_max": [25], "temperature_2m_min": [15], "precipitation_sum": [0]}
    }
    mock_requests_get.return_value = mock_response

    result = tool.execute()
    assert "Weather Report for London,UK" in result
    assert "Current Temperature: 20°C" in result


def test_weather_tool_parameters_schema():
    tool = WeatherTool()
    schema = tool.get_parameters_schema()
    assert schema["type"] == "object"
    assert "location" in schema["properties"]
    assert "location" in schema["required"]