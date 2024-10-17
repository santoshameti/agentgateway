# Building Custom Tools

Creating custom tools allows you to extend the AI Agent Gateway's capabilities to suit your specific needs. Follow these steps to build a custom tool:

1. Create a new Python file in the `tools/` directory (e.g., `custom_tool.py`).

2. Import the necessary modules:
   ```python
   from core.abstract_tool import Tool
   ```

3. Define your custom tool class, inheriting from `Tool`:
   ```python
   class CustomTool(Tool):
       def __init__(self):
           super().__init__("custom_tool_name", "Description of your custom tool")
   ```

4. Implement the required methods:
   ```python
   def execute(self):
       # Main logic of your tool
       pass

   def get_parameters_schema(self):
       return {
           "type": "object",
           "properties": {
               "param1": {"type": "string", "description": "Description of param1"},
               "param2": {"type": "integer", "description": "Description of param2"}
           },
           "required": ["param1"]
       }

   def is_auth_setup(self):
       # Check if authentication is properly set up
       return "api_key" in self.auth_data
   ```

5. If your tool requires authentication, implement the `set_auth` method:
   ```python
   def set_auth(self, **kwargs):
       if "api_key" not in kwargs:
           raise ValueError("API key is required for CustomTool")
       self.auth_data["api_key"] = kwargs["api_key"]
   ```

6. Optionally, add any helper methods or additional functionality specific to your tool.

Remember to thoroughly test your custom tool and document its usage for other developers.
