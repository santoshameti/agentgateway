# API Reference: Response

The `Response` class represents the output from an AI agent.

## Class: Response

### Constructor

```python
Response(content: str, metadata: Dict[str, Any] = None)
```

- `content`: A string containing the main content of the response.
- `metadata`: (Optional) A dictionary containing additional metadata about the response.

### Methods

#### get_content

```python
get_content() -> str
```

Retrieves the main content of the response.

Returns: The response content as a string.

#### get_metadata

```python
get_metadata() -> Dict[str, Any]
```

Retrieves the metadata associated with the response.

Returns: A dictionary containing the response metadata.

#### set_metadata

```python
set_metadata(key: str, value: Any)
```

Sets or updates a specific metadata key-value pair.

- `key`: The metadata key as a string.
- `value`: The value to be associated with the key.

### Properties

#### content

```python
@property
def content() -> str
```

Returns the main content of the response.

#### metadata

```python
@property
def metadata() -> Dict[str, Any]
```

Returns the metadata dictionary associated with the response.

