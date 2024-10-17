# Integrating Adapters

Once you've created a custom adapter, you need to integrate it into the AI Agent Gateway. Follow these steps:

1. Update the `AgentType` enum in `agent_gateway.py`:
   ```python
   from enum import Enum

   class AgentType(Enum):
       # Existing types...
       CUSTOM_AI = "custom_ai"
   ```

2. Import your custom adapter in `agent_gateway.py`:
   ```python
   from adapters.custom_ai_adapter import CustomAIAdapter
   ```

3. Update the `create_agent` method in the `AgentGateway` class:
   ```python
   def create_agent(self, prompt, tools=None):
       if self.agent_type == AgentType.CUSTOM_AI:
           return CustomAIAdapter(model_id=self.model_id)
       # Existing code for other agent types...
   ```

4. If your adapter requires specific initialization or configuration, add it to the `AgentGateway` class:
   ```python
   def configure_custom_ai(self, **kwargs):
       if self.agent_type != AgentType.CUSTOM_AI:
           raise ValueError("Agent type is not CUSTOM_AI")
       self.adapter.set_auth(**kwargs)
       # Any other necessary configuration
   ```

5. Update the documentation to include information about the new adapter and its usage.

6. Add appropriate tests for the new adapter in the `tests/adapters/` directory.

By following these steps, you'll successfully integrate your custom adapter into the AI Agent Gateway, allowing users to leverage your new AI backend alongside existing options.
