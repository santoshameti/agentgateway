# API Reference: Prompt

The `Prompt` class represents the instructions or context given to an AI agent.

## Class: Prompt

### Constructor

```python
Prompt(content: str)
```

- `content`: A string containing the prompt or instructions for the agent.

### Methods

#### get_content

```python
get_content() -> str
```

Retrieves the content of the prompt.

Returns: The prompt content as a string.

#### set_content

```python
set_content(content: str)
```

Sets or updates the content of the prompt.

- `content`: The new prompt content as a string.

#### append_content

```python
append_content(additional_content: str)
```

Appends additional content to the existing prompt.

- `additional_content`: The content to be appended to the prompt.

### Properties

#### content

```python
@property
def content() -> str
```

Returns the current content of the prompt.

```python
@content.setter
def content(value: str)
```

Sets the content of the prompt.

