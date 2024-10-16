import json
from typing import Dict, Any
from core.abstract_tool import Tool
from anthropic import Anthropic


class TopicDetectionTool(Tool):
    def __init__(self, model_id=""):
        super().__init__("detect_topics", "Detect main topics in a given text")
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
        num_topics = parameters.get('num_topics', 5)

        client = Anthropic(api_key=self.auth_data['api_key'])

        prompt = f"""Analyze the following text and identify the top {num_topics} main topics. For each topic, provide a short label and the top 3 related words.

        Text: {text}

        Topics:"""

        response = client.messages.create(
            model=self.model_id,
            max_tokens=200,
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        topics_text = response.content[0].text.strip()

        # Parse the response to extract topics
        topics = []
        for line in topics_text.split('\n'):
            if ':' in line:
                label, words = line.split(':')
                topics.append({
                    "label": label.strip(),
                    "words": [word.strip() for word in words.split(',')]
                })

        return json.dumps(topics)

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to analyze for topic detection"
                },
                "num_topics": {
                    "type": "integer",
                    "description": "The number of topics to detect",
                    "default": 5
                }
            },
            "required": ["text"]
        }