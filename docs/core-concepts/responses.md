# Responses

In the AI Agent Gateway system, Responses encapsulate the output from agents, including answers, tool calls, and error messages. The `Response` class provides a structured way to handle different types of agent outputs.

## Response Structure

A Response object consists of the following components:

1. **Content**: The main text content of the response.
2. **Response Type**: An enumeration indicating the type of response.
3. **Tools**: A list of tools that the agent wants to use (if applicable).

## Response Types

The `ResponseType` enum defines the possible types of responses:

- `ANSWER`: A final answer from the agent.
- `TOOL_CALL`: A request to use one or more tools.
- `ERROR`: An error message indicating a problem during execution.

## Response Class

The `Response` class is the core structure for handling agent outputs. Here's an overview of its key components:

### Properties

- `content`: The main text content of the response.
- `response_type`: The type of response (ANSWER, TOOL_CALL, or ERROR).
- `tools`: A list of tools that the agent wants to use (only applicable for TOOL_CALL responses).

### Methods

#### `__init__(self, content: str, response_type: ResponseType, tools: List[Tool] = None)`
Initializes a new Response object.

- **Parameters:**
  - `content`: The main text content of the response.
  - `response_type`: The type of response (from the ResponseType enum).
  - `tools`: An optional list of tools (only used for TOOL_CALL responses).

#### `get_tools(self) -> List[Tool]`
Returns the list of tools associated with the response (if any).

#### `to_dict(self) -> Dict[str, Any]`
Converts the Response object to a dictionary representation.

## Usage Examples

### Creating an ANSWER Response

```python
from core.response import Response, ResponseType

answer_response = Response("The capital of France is Paris.", ResponseType.ANSWER)
```

### Creating a TOOL_CALL Response

```python
from core.response import Response, ResponseType
from tools.weather_tool import WeatherTool

weather_tool = WeatherTool()
tool_call_response = Response("I need to check the weather.", ResponseType.TOOL_CALL, tools=[weather_tool])
```

### Creating an ERROR Response

```python
from core.response import Response, ResponseType

error_response = Response("An error occurred while processing the request.", ResponseType.ERROR)
```

## Handling Responses

When working with the AI Agent Gateway, you'll typically handle responses in the following ways:

1. Check the `response_type` to determine how to process the response.
2. For ANSWER responses, use the `content` directly as the final output.
3. For TOOL_CALL responses, execute the requested tools and provide their output back to the agent.
4. For ERROR responses, handle the error condition appropriately in your application.

Example:

```python
def process_response(response: Response):
    if response.response_type == ResponseType.ANSWER:
        print(f"Final answer: {response.content}")
    elif response.response_type == ResponseType.TOOL_CALL:
        for tool in response.get_tools():
            tool_output = tool.execute()
            # Process tool output and potentially feed it back to the agent
    elif response.response_type == ResponseType.ERROR:
        print(f"Error occurred: {response.content}")
        # Handle the error condition
```

By using the Response class and its associated types, you can create a robust system for handling various outputs from your AI agents, including multi-step processes involving tool usage.
