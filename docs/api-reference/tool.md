# API Reference: Tool

The `Tool` class is an abstract base class for all tool implementations in the AI Agent Gateway.

## Class: Tool (Abstract Base Class)

### Constructor

```python
Tool(name: str, description: str)
```

- `name`: A string representing the name of the tool.
- `description`: A string providing a brief description of the tool's functionality.

### Abstract Methods

#### execute

```python
@abstractmethod
def execute() -> Any
```

Executes the tool's main functionality. Must be implemented by subclasses.

Returns: The result of the tool's execution.

#### get_parameters_schema

```python
@abstractmethod
def get_parameters_schema() -> Dict[str, Any]
```

Retrieves the JSON schema for the tool's parameters. Must be implemented by subclasses.

Returns: A dictionary representing the JSON schema of the tool's parameters.

#### is_auth_setup

```python
@abstractmethod
def is_auth_setup() -> bool
```

Checks if the tool's authentication is properly configured. Must be implemented by subclasses.

Returns: A boolean indicating whether authentication is set up.

### Methods

#### set_auth

```python
set_auth(**kwargs)
```

Sets the authentication data for the tool.

- `**kwargs`: Key-value pairs of authentication data.

#### get_auth

```python
get_auth() -> Dict[str, Any]
```

Retrieves the current authentication data.

Returns: A dictionary containing the current authentication data.

#### set_parameters

```python
set_parameters(parameters: Dict[str, Any])
```

Sets the parameters for the tool.

- `parameters`: A dictionary of parameters to set.

#### get_parameters

```python
get_parameters() -> Dict[str, Any]
```

Retrieves the current parameters of the tool.

Returns: A dictionary of the tool's parameters.

#### set_instance_id

```python
set_instance_id(instance_id: str)
```

Sets the instance ID for the tool.

- `instance_id`: A string representing the unique instance ID.

#### get_instance_id

```python
get_instance_id() -> str
```

Retrieves the instance ID of the tool.

Returns: The instance ID as a string.

### Properties

#### name

```python
@property
def name() -> str
```

Returns the name of the tool.

#### description

```python
@property
def description() -> str
```

Returns the description of the tool.

