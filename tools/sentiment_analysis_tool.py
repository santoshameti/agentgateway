import json
from typing import Dict, Any
from core.abstract_tool import Tool
from anthropic import Anthropic


class SentimentAnalysisTool(Tool):
    def __init__(self):
        super().__init__("analyze_sentiment", "Analyze the sentiment of text")
        self.model_id = "claude-3-haiku-20240307"

    def is_auth_setup(self):
        return 'api_key' in self.auth_data

    def execute(self) -> Any:
        if not self.is_auth_setup():
            raise ValueError("API key not set. Use set_auth() to set the API key.")

        parameters = self.get_parameters()
        text = parameters.get('text')

        client = Anthropic(api_key=self.auth_data['api_key'])

        prompt = f"""Analyze the sentiment of the following text. Provide a sentiment label (positive, negative, or neutral) and a confidence score between 0 and 1.

        Text: {text}

        Sentiment analysis:"""

        response = client.messages.create(
            model=self.model_id,
            max_tokens=100,
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        analysis = response.content[0].text.strip()

        # Parse the response to extract sentiment and score
        lines = analysis.split('\n')
        sentiment = lines[0].split(':')[1].strip().lower() if len(lines) > 0 else "unknown"
        score = float(lines[1].split(':')[1].strip()) if len(lines) > 1 else 0.0

        response = {
            "sentiment": sentiment,
            "score": score
        }

        return json.dumps(response)

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to analyze for sentiment"
                }
            },
            "required": ["text"]
        }