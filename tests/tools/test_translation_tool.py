import pytest
from tools.translate_tool import TranslationTool
from unittest.mock import patch, MagicMock


def test_translation_tool_initialization():
    tool = TranslationTool()
    assert tool.name == "translate"
    assert tool.description == "Translate text from one language to another"


def test_translation_tool_is_auth_setup():
    tool = TranslationTool()
    assert tool.is_auth_setup() == False
    tool.set_auth(api_key="test_key")
    assert tool.is_auth_setup() == True


@patch('tools.translate_tool.Anthropic')
def test_translation_tool_execute(mock_anthropic_class):
    # Setup the mock
    mock_anthropic_instance = MagicMock()
    mock_anthropic_class.return_value = mock_anthropic_instance

    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="Hola")]
    mock_anthropic_instance.messages.create.return_value = mock_message

    # Create and setup the tool
    tool = TranslationTool()
    tool.set_auth(api_key="test_key")
    tool.set_parameter("text", "Hello")
    tool.set_parameter("source_lang", "en")
    tool.set_parameter("target_lang", "es")

    # Execute the tool
    result = tool.execute()

    # Assertions
    assert result == "Hola"
    mock_anthropic_instance.messages.create.assert_called_once()
    call_kwargs = mock_anthropic_instance.messages.create.call_args.kwargs
    assert call_kwargs['model'] == tool.model_id
    assert call_kwargs['max_tokens'] == 4096
    assert call_kwargs['temperature'] == 0
    assert len(call_kwargs['messages']) == 1
    assert call_kwargs['messages'][0]['role'] == 'user'
    assert "Translate the following text from en to es: 'Hello'" in call_kwargs['messages'][0]['content']


def test_translation_tool_parameters_schema():
    tool = TranslationTool()
    schema = tool.get_parameters_schema()
    assert schema["type"] == "object"
    assert all(param in schema["properties"] for param in ["text", "source_lang", "target_lang"])
    assert all(param in schema["required"] for param in ["text", "source_lang", "target_lang"])


@patch('tools.translate_tool.Anthropic')
def test_translation_tool_execute_api_error(mock_anthropic_class):
    # Setup the mock to raise an exception
    mock_anthropic_instance = MagicMock()
    mock_anthropic_class.return_value = mock_anthropic_instance
    mock_anthropic_instance.messages.create.side_effect = Exception("API Error")

    # Create and setup the tool
    tool = TranslationTool()
    tool.set_auth(api_key="test_key")
    tool.set_parameter("text", "Hello")
    tool.set_parameter("source_lang", "en")
    tool.set_parameter("target_lang", "es")

    # Execute the tool and expect an exception
    with pytest.raises(Exception, match="API Error"):
        tool.execute()