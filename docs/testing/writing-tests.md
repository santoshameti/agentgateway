# Writing Tests

This guide provides best practices and examples for writing tests for the AI Agent Gateway project.

## Test Structure

1. Place test files in the appropriate subdirectory of the `tests/` folder.
2. Name test files with the prefix `test_` (e.g., `test_weather_tool.py`).
3. Use descriptive names for test functions, prefixed with `test_`.

Example test structure:

```python
import pytest
from unittest.mock import patch
from tools.weather_tool import WeatherTool

@pytest.fixture
def weather_tool():
    return WeatherTool()

def test_weather_tool_execution(weather_tool):
    with patch('tools.weather_tool.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"temperature": 20}
        weather_tool.set_parameters({"location": "London"})
        result = weather_tool.execute()
        assert "temperature" in result
        assert result["temperature"] == 20

# More test functions...
```

## Best Practices

1. Test all public methods of each class.
2. Include both positive and negative test cases.
3. Test edge cases and error handling.
4. Use parameterized tests for testing multiple input scenarios.
5. Mock external API calls to ensure tests can run without network requests.
6. Keep tests isolated and independent of each other.
7. Use clear and descriptive assert statements.

## Using Fixtures

Pytest fixtures are useful for setting up test environments:

```python
import pytest
from agent_gateway import AgentGateway, AgentType

@pytest.fixture
def agent_gateway():
    gateway = AgentGateway(AgentType.OPENAI)
    gateway.adapter.set_auth(api_key="test_key")
    return gateway

def test_agent_creation(agent_gateway):
    agent = agent_gateway.create_agent("Test prompt")
    assert agent is not None
    # More assertions...
```

## Mocking

Use mocking to simulate external dependencies:

```python
from unittest.mock import patch, MagicMock

def test_openai_adapter_run():
    with patch('adapters.openai_adapter.openai.Completion.create') as mock_create:
        mock_create.return_value = MagicMock(choices=[MagicMock(text="Mocked response")])
        adapter = OpenAIAdapter()
        response = adapter.run("Test input", False)
        assert response.content == "Mocked response"
```

## Parameterized Tests

Use parameterized tests for multiple input scenarios:

```python
import pytest

@pytest.mark.parametrize("input_text,expected_output", [
    ("Hello", "HELLO"),
    ("world", "WORLD"),
    ("OpenAI", "OPENAI"),
])
def test_uppercase_conversion(input_text, expected_output):
    assert input_text.upper() == expected_output
```

By following these guidelines and examples, you can create comprehensive and effective tests for the AI Agent Gateway project, ensuring its reliability and maintainability.
