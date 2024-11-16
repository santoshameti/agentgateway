from typing import Dict, Any
from agentgateway.core.abstract_tool import Tool

class CalculatorTool(Tool):
    def __init__(self):
        super().__init__("calculate", "Perform basic arithmetic calculations")

    def is_auth_setup(self):
        return True

    def execute(self) -> Any:
        parameters = self.get_parameters()
        expression = parameters.get('expression')
        try:
            result = eval(expression)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The arithmetic expression to evaluate, e.g., '2 + 2'"
                }
            },
            "required": ["expression"]
        }