# Agent Gateway

The Agent Gateway is the central component of the AI Agent Gateway system. It acts as a facade, providing a unified interface to interact with various AI backends and tools.

## Overview

The `AgentGateway` class is responsible for:

1. Initializing and managing the appropriate AI backend adapter
2. Preparing the agent with instructions and tools
3. Running the agent and handling its responses
4. Managing tool execution based on the agent's requests

## Key Components

### AgentType Enum

The `AgentType` enum defines the supported AI backends:

- BEDROCK
- OPENAI
- VERTEX (coming soon)
- ANTHROPIC
- GROQ
- TOGETHER
- FIREWORKS

### Initialization

The `AgentGateway` can be initialized with either an `AgentType` or an `AbstractAgent`:

```python
gateway = AgentGateway(AgentType.ANTHROPIC, model_id="claude-3-5-sonnet-20240620")
# or
gateway = AgentGateway(custom_agent_adapter, model_id="custom_model")
```

### Preparing the Agent

Before running the agent, you need to prepare it with instructions and tools:

```python
gateway.prepare_agent(prompt, tools=[tool1, tool2, ...])
```

This method:
- Sets the agent's instructions based on the provided prompt
- Adds the specified tools to the agent
- Validates that each tool's authentication is properly set up

### Running the Agent

The `run_agent` method is the main entry point for interacting with the AI:

```python
result = gateway.run_agent(agent_input)
```

This method:
- Sends the input to the AI backend
- Handles tool calls if the AI requests to use a tool
- Continues the conversation until a final answer is reached
- Returns the final answer from the AI

## Error Handling

The `AgentGateway` includes custom error handling:

- `UnsupportedAgentException`: Raised when an unsupported agent type is specified
- Various checks for tool authentication and validity

## Logging

The `AgentGateway` uses the `AgentLogger` for logging various steps and potential issues during the agent's lifecycle.

## Next Steps

To learn more about the components that interact with the Agent Gateway, check out the following sections:

- [Agents](agents.md)
- [Prompts](prompts.md)
- [Responses](responses.md)
- [Tools](tools.md)
