# API Reference: Agent

The `Agent` class represents an AI agent with specific instructions and optional tools.

## Class: Agent

### Constructor

```python
Agent(instructions: str, tools: List[Tool] = None)
```

- `instructions`: A string containing the agent's instructions or prompt.
- `tools`: (Optional) A list of `Tool` objects available to the agent.

### Methods

#### add_tool

```python
add_tool(tool: Tool)
```

Adds a new tool to the agent's toolkit.

- `tool`: A `Tool` object to be added.

#### remove_tool

```python
remove_tool(tool_name: str)
```

Removes a tool from the agent's toolkit.

- `tool_name`: The name of the tool to be removed.

#### execute_tool

```python
execute_tool(tool_name: str, parameters: Dict[str, Any]) -> Any
```

Executes a specific tool with the given parameters.

- `tool_name`: The name of the tool to execute.
- `parameters`: A dictionary of parameters for the tool.

Returns: The result of the tool execution.

#### get_conversation_history

```python
get_conversation_history() -> List[Dict[str, Any]]
```

Retrieves the conversation history.

Returns: A list of dictionaries containing the conversation history.

#### clear_conversation_history

```python
clear_conversation_history()
```

Clears the conversation history.

#### add_to_conversation_history

```python
add_to_conversation_history(role: str, content: str)
```

Adds a new message to the conversation history.

- `role`: The role of the message sender (e.g., "user", "assistant", "system").
- `content`: The content of the message.

### Properties

#### instructions

```python
@property
def instructions() -> str
```

Returns the agent's instructions or prompt.

#### tools

```python
@property
def tools() -> List[Tool]
```

Returns the list of tools available to the agent.

