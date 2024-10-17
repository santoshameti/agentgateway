# Tool Authentication

Many tools require authentication to access external services. The AI Agent Gateway provides a consistent way to handle tool authentication:

1. Setting Authentication:
   - Use the `set_auth` method to provide authentication details.
   - Example: `tool.set_auth(api_key="your_api_key_here")`

2. Checking Authentication:
   - Implement the `is_auth_setup` method to verify if the necessary authentication is in place.
   - Return `True` if authentication is properly set up, `False` otherwise.

3. Accessing Authentication Data:
   - Use `self.auth_data` within your tool to access stored authentication information.
   - Example: `api_key = self.auth_data.get("api_key")`

4. Secure Handling:
   - Never log or display full authentication details (like API keys).
   - Use environment variables or secure storage solutions for sensitive information.

5. Error Handling:
   - Raise clear exceptions if required authentication is missing or invalid.

Remember to document the authentication requirements for each tool, including the expected format and any necessary setup steps.
