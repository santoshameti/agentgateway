import requests
from typing import Dict, Any
from agentgateway.core.abstract_tool import Tool

class AskUserTool(Tool):
    def __init__(self):
        super().__init__("ask_user",
                         "This tool is to get input from a user. Pick the tool to set the question to ask for user input")

    def is_auth_setup(self):
        return True

    def execute(self) -> Any:
        parameters = self.get_parameters()
        question = parameters.get('question')
        clarification = input(f"Agent needs clarification: {question}\nYour response: ")
        return clarification

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Question you want to ask user to get their input"
                }
            },
            "required": ["question"]
        }