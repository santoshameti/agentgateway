from typing import Dict, Any
from agentgateway.core.abstract_tool import Tool
from anthropic import Anthropic

class TranslationTool(Tool):
    def __init__(self):
        super().__init__("translate", "Translate text from one language to another")
        self.model_id = "claude-3-haiku-20240307"

    def is_auth_setup(self):
        if 'api_key' not in self.auth_data:
            return False

        return True

    def execute(self) -> Any:
        if 'api_key' not in self.auth_data:
            raise ValueError("API key not set. Use set_auth() to set the API key.")
        parameters = self.get_parameters()
        text = parameters.get('text')
        source_lang = parameters.get('source_lang')
        target_lang = parameters.get('target_lang')

        # This is a mock implementation. In a real scenario, you would use a translation API.
        translated_text = self.translate_text(text, source_lang, target_lang)
        return translated_text

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to translate"
                },
                "source_lang": {
                    "type": "string",
                    "description": "The source language code (e.g., 'en' for English)"
                },
                "target_lang": {
                    "type": "string",
                    "description": "The target language code (e.g., 'es' for Spanish)"
                }
            },
            "required": ["text", "source_lang", "target_lang"]
        }

    def translate_text(self, text, source_lang, target_lang):
        client = Anthropic(api_key = self.auth_data['api_key'])

    # Construct the message for Claude
        message = f"Translate the following text from {source_lang} to {target_lang}: '{text}'"

    # Make the API call
        response = client.messages.create(
            model=self.model_id,
            max_tokens=4096,
            temperature=0,
            messages=[
                {"role": "user", "content": message}
            ]
        )

    # Extract the translated text from the response
        translated_text = response.content[0].text
        return translated_text