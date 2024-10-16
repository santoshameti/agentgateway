import json
from typing import Dict, Any
from core.abstract_tool import Tool
from tools.askuser_tool import AskUserTool
from tools.weather_tool import WeatherTool
from tools.calculator_tool import CalculatorTool
from tools.translate_tool import TranslationTool
from tools.web_search_tool import WebSearchTool
from utils.agent_logger import AgentLogger
from tools.sentiment_analysis_tool import SentimentAnalysisTool
from tools.topic_detection_tool import TopicDetectionTool
from tools.text_summarization_tool import TextSummarizationTool

class ToolManager:
    def __init__(self):
        self.logging = AgentLogger("Agent")

    def get_tool(self, tool_data: Dict[str, Any]) -> Tool:
        self.logging.info("ToolManager:get_tool:function called")
        tool_name = tool_data.get('name')
        input_params = tool_data.get('input', {})
        if isinstance(input_params, str):
            input_params = json.loads(input_params)
        instance_id = tool_data.get('id')
        self.logging.info(f"ToolManager:get_tool:tool name requested {tool_name}")

        if tool_name == "ask_user":
            tool = AskUserTool()
        elif tool_name == "get_weather":
            tool = WeatherTool()
        elif tool_name == "calculate":
            tool = CalculatorTool()
        elif tool_name == "translate":
            tool = TranslationTool()
        elif tool_name == "web_search":
            tool = WebSearchTool()
        elif tool_name == "analyze_sentiment":
            tool = SentimentAnalysisTool()
        elif tool_name == "detect_topics":
            tool = TopicDetectionTool()
        elif tool_name == "summarize_text":
            tool = TextSummarizationTool()
        else:
            self.logging.info(f"ToolManager:get_tool:Tool name not found {tool_name}")
            raise ValueError(f"Unknown tool: {tool_name}")

        tool.set_instance_id(instance_id)

        self.logging.info(f"ToolManager:get_tool: setting parameters for the tool {tool_name}")
        # Validate and set input parameters
        self._validate_and_set_input(tool, input_params)
        self.logging.info(f"ToolManager:get_tool: setting parameters completed for the tool {tool_name}")
        return tool

    def _validate_and_set_input(self, tool: Tool, input_params: Dict[str, Any]):
        self.logging.info(f"ToolManager:_validate_and_set_input: setting input parameters for the tool {tool.name}")
        schema = tool.get_parameters_schema()
        properties = schema.get('properties', {})
        required = schema.get('required', [])

        # Check for required parameters
        for param in required:
            if param not in input_params:
                raise ValueError(f"Missing required parameter: {param}")

        # Validate and set parameters
        for key, value in input_params.items():
            if key not in properties:
                raise ValueError(f"Unexpected parameter: {key}")

            expected_type = properties[key]['type']
            if not self._check_type(value, expected_type):
                raise TypeError(
                    f"Invalid type for parameter '{key}'. Expected {expected_type}, got {type(value).__name__}")

            self.logging.info(f"ToolManager:get_tool: setting parameters for the tool {tool.name}")
            tool.set_parameter(key, value)

    def _check_type(self, value: Any, expected_type: str) -> bool:
        if expected_type == 'string':
            return isinstance(value, str)
        elif expected_type == 'number':
            return isinstance(value, (int, float))
        elif expected_type == 'integer':
            return isinstance(value, int)
        elif expected_type == 'boolean':
            return isinstance(value, bool)
        elif expected_type == 'array':
            return isinstance(value, list)
        elif expected_type == 'object':
            return isinstance(value, dict)
        else:
            return True

    def _validate_input(self, tool: Tool, input_params: Dict[str, Any]):
        schema = tool.get_parameters_schema()
        required_params = schema.get('required', [])
        properties = schema.get('properties', {})

        # Check for required parameters
        for param in required_params:
            if param not in input_params:
                raise ValueError(f"Missing required parameter: {param}")

        # Check parameter types
        for param, value in input_params.items():
            if param in properties:
                expected_type = properties[param]['type']
                if not self._check_type(value, expected_type):
                    raise TypeError(
                        f"Invalid type for parameter '{param}'. Expected {expected_type}, got {type(value).__name__}")

    def _check_type(self, value: Any, expected_type: str) -> bool:
        if expected_type == 'string':
            return isinstance(value, str)
        elif expected_type == 'number':
            return isinstance(value, (int, float))
        elif expected_type == 'integer':
            return isinstance(value, int)
        elif expected_type == 'boolean':
            return isinstance(value, bool)
        elif expected_type == 'array':
            return isinstance(value, list)
        elif expected_type == 'object':
            return isinstance(value, dict)
        else:
            return True  # For any other types, we'll assume it's valid
