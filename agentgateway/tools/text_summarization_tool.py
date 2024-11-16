from typing import Dict, Any
from agentgateway.core.abstract_tool import Tool
from anthropic import Anthropic


class TextSummarizationTool(Tool):
    def __init__(self, model_id=""):
        super().__init__("summarize_text", "Summarize long pieces of text")
        if model_id != "":
            self.model_id = model_id
        else:
            self.model_id = "claude-3-haiku-20240307"

    def is_auth_setup(self):
        return 'api_key' in self.auth_data

    def execute(self) -> Any:
        if not self.is_auth_setup():
            raise ValueError("API key not set. Use set_auth() to set the API key.")

        parameters = self.get_parameters()
        text = parameters.get('text')
        max_length = parameters.get('max_length', 130)
        min_length = parameters.get('min_length', 30)

        client = Anthropic(api_key=self.auth_data['api_key'])

        prompt = f"""Summarize the following text in {min_length} to {max_length} words:

        {text}

        Summary:"""

        response = client.messages.create(
            model=self.model_id,
            max_tokens=max_length * 2,  # Giving some extra tokens for flexibility
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text.strip()

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to summarize"
                },
                "max_length": {
                    "type": "integer",
                    "description": "The maximum length of the summary in words",
                    "default": 130
                },
                "min_length": {
                    "type": "integer",
                    "description": "The minimum length of the summary in words",
                    "default": 30
                }
            },
            "required": ["text"]
        }