import json
from typing import Dict, Any
from agentgateway.core.abstract_tool import Tool
from textblob import TextBlob


class SentimentAnalysisTool(Tool):
    def __init__(self):
        super().__init__("analyze_sentiment", "Analyze the sentiment of text")

    def is_auth_setup(self):
        return True

    def execute(self) -> str:
        parameters = self.get_parameters()
        text = parameters.get('text')

        if not text:
            raise ValueError("No text provided for sentiment analysis.")

        # Analyze the text using TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        # Determine the sentiment based on polarity
        if polarity > 0:
            sentiment = "positive"
        elif polarity < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        response = {
            "sentiment": sentiment,
            "score": polarity
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