# Agents

Agents are the core entities in the AI Agent Gateway system that process user inputs, execute tasks, and generate responses. They are built on top of various AI models and can be extended with additional tools and capabilities.

## Agent Components

An agent consists of three main components:

1. **Instructions**: The base prompt or set of guidelines that define the agent's behavior and capabilities.
2. **Tools**: Additional functionalities that the agent can use to perform specific tasks.
3. **User Input**: The queries or commands provided by the user that the agent processes.

Here's a diagram illustrating the structure of an agent:

<antArtifact identifier="agent-diagram" type="image/svg+xml" title="Agent Structure Diagram">
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="500" height="300" fill="#f0f0f0" stroke="#000000" stroke-width="2"/>
  <text x="300" y="30" text-anchor="middle" font-size="24" font-weight="bold">Agent</text>
  <!-- Instructions -->
  <rect x="75" y="75" width="150" height="100" fill="#b3e0ff" stroke="#000000" stroke-width="2"/>
  <text x="150" y="130" text-anchor="middle" font-size="18">Instructions</text>
  <!-- Tools -->
  <rect x="250" y="75" width="150" height="100" fill="#ffd9b3" stroke="#000000" stroke-width="2"/>
  <text x="325" y="130" text-anchor="middle" font-size="18">Tools</text>
  <!-- User Input -->
  <rect x="75" y="200" width="450" height="50" fill="#d9f2d9" stroke="#000000" stroke-width="2"/>
  <text x="300" y="230" text-anchor="middle" font-size="18">User Input</text>
  <!-- Output -->
  <rect x="75" y="275" width="450" height="50" fill="#ffcccc" stroke="#000000" stroke-width="2"/>
  <text x="300" y="305" text-anchor="middle" font-size="18">Output</text>
  <!-- Arrows -->
  <path d="M150 175 L150 200" stroke="#000000" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <path d="M325 175 L325 200" stroke="#000000" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <path d="M300 250 L300 275" stroke="#000000" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <!-- Arrowhead definition -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" />
    </marker>
  </defs>
</svg>

## Abstract Agent

The `AbstractAgent` class serves as the base class for all agent implementations. It defines the common interface and functionality that all agents should have. Here's a detailed overview of the `AbstractAgent` class:

### Properties

- `instructions`: The base prompt or guidelines for the agent.
- `tools`: A dictionary of tools available to the agent, keyed by tool name.
- `model`: The identifier for the AI model being used.

### Methods

#### `__init__(self, model: str)`
Initializes a new agent with the specified model.

#### `set_instructions(self, instructions: str)`
Sets the base instructions for the agent.

- **Parameters:**
  - `instructions`: A string containing the instructions or prompt for the agent.

#### `add_tool(self, tool: Tool)`
Adds a tool to the agent's toolset.

- **Parameters:**
  - `tool`: An instance of a Tool class to be added to the agent.

#### `remove_tool(self, tool_name: str)`
Removes a tool from the agent's toolset.

- **Parameters:**
  - `tool_name`: The name of the tool to be removed.

#### `get_tools(self) -> List[Tool]`
Returns a list of all tools available to the agent.

#### `run(self, user_input: str, is_tool_response: bool = False) -> Response`
Processes the user input and returns a response. This is an abstract method that must be implemented by subclasses.

- **Parameters:**
  - `user_input`: The input provided by the user.
  - `is_tool_response`: A boolean indicating whether the input is a response from a tool.
- **Returns:**
  - A Response object containing the agent's output.

#### `get_formatted_tool_output(self, tool: Tool, tool_output: Any) -> str`
Formats the output of a tool execution. This is an abstract method that must be implemented by subclasses.

- **Parameters:**
  - `tool`: The Tool instance that was executed.
  - `tool_output`: The output from the tool's execution.
- **Returns:**
  - A formatted string representation of the tool's output.

### Abstract Methods

The following methods are abstract and must be implemented by any concrete agent class:

- `run(self, user_input: str, is_tool_response: bool = False) -> Response`
- `get_formatted_tool_output(self, tool: Tool, tool_output: Any) -> str`

## Agent Lifecycle

1. **Initialization**: An agent is created with a specific AI model.
2. **Configuration**: The agent is configured with instructions and tools.
3. **Execution**: The agent processes user input, potentially using tools as needed.
4. **Response**: The agent generates a response based on the input and any tool outputs.

## Extending Agents

To create a new agent type:

1. Create a new class that inherits from `AbstractAgent`.
2. Implement the required abstract methods: `run` and `get_formatted_tool_output`.
3. Add any additional methods or properties specific to your agent type.

Example:

```python
from core.abstract_agent import AbstractAgent
from core.response import Response
from core.abstract_tool import Tool
from typing import Any, List

class MyCustomAgent(AbstractAgent):
    def __init__(self, model: str):
        super().__init__(model)
        # Add any custom initialization here

    def run(self, user_input: str, is_tool_response: bool = False) -> Response:
        # Implement the logic for processing user input and generating a response
        # This might involve calling the AI model, using tools, etc.
        pass

    def get_formatted_tool_output(self, tool: Tool, tool_output: Any) -> str:
        # Implement the logic for formatting tool output
        pass

    # Add any other custom methods as needed
```

By following this structure, you can create agents that work seamlessly with the AI Agent Gateway while providing custom functionality for specific use cases or AI backends.
