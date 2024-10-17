# Built-in Tools

The AI Agent Gateway comes with several pre-implemented tools to cover common use cases:

1. WeatherTool
   - Purpose: Retrieves weather information for specified locations.
   - Parameters: location (string)
   - Authentication: Requires a weather API key

2. CalculatorTool
   - Purpose: Performs basic mathematical calculations.
   - Parameters: expression (string)
   - Authentication: None required

3. TranslationTool
   - Purpose: Translates text between different languages.
   - Parameters: text (string), source_language (string), target_language (string)
   - Authentication: Requires a translation API key

4. AskUserTool
   - Purpose: Allows the agent to request additional information from the user.
   - Parameters: question (string)
   - Authentication: None required

These built-in tools provide a foundation for common tasks and serve as examples for creating custom tools.
