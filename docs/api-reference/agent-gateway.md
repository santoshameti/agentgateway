# API Reference: Agent Gateway

The `AgentGateway` class is the main entry point for interacting with the AI Agent Gateway.

## Class: AgentGateway

### Constructor

```python
AgentGateway(agent_type: AgentType, model_id: str = "")
```

- `agent_type`: An `AgentType` enum value specifying the AI backend to use.
- `model_id`: (Optional) A string specifying the model ID for the chosen AI backend.

### Methods

#### create_agent

```python
create_agent(prompt: Prompt, tools: List[Tool] = None) -> Agent
```

Creates a new agent with the specified prompt and optional tools.

- `prompt`: A `Prompt` object containing the agent's instructions.
- `tools`: (Optional) A list of `Tool` objects to be used by the agent.

Returns: An `Agent` object.

#### run_agent

```python
run_agent(agent: Agent, input_message: str) -> Response
```

Runs the specified agent with the given input message.

- `agent`: An `Agent` object created by `create_agent`.
- `input_message`: A string containing the user's input or query.

Returns: A `Response` object containing the agent's output.

#### set_model_config

```python
set_model_config(**kwargs)
```

Sets or updates the model configuration for the current adapter.

- `**kwargs`: Key-value pairs of configuration options specific to the current AI backend.

#### get_model_config

```python
get_model_config() -> Dict[str, Any]
```

Retrieves the current model configuration.

Returns: A dictionary containing the current model configuration.

### Properties

#### adapter

```python
@property
def adapter() -> AbstractAgent
```

Returns the current adapter instance based on the selected agent type.

#### model_id

```python
@property
def model_id() -> str
```

Returns the current model ID.

