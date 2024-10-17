# Adapters Overview

Adapters in the AI Agent Gateway serve as interfaces between the gateway and various AI backends. They provide a unified way to interact with different AI models and services, abstracting away the specifics of each backend's API.

Key points about adapters:

1. Adapters implement the `AbstractAgent` interface.
2. Each adapter is responsible for communicating with a specific AI backend (e.g., OpenAI, Anthropic, Bedrock).
3. Adapters handle authentication, request formatting, and response parsing for their respective backends.
4. The AI Agent Gateway uses adapters to create and run agents with different AI models seamlessly.

Adapters play a crucial role in making the AI Agent Gateway flexible and extensible, allowing easy integration of new AI backends as they become available.
