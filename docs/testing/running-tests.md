# Running Tests

This guide explains how to run tests for the AI Agent Gateway project.

## Prerequisites

Ensure you have pytest installed. If not, install it using:

```
pip install -r requirements.txt
```

## Running All Tests

From the root directory of the project, run:

```
python -m pytest
```

This command will discover and run all tests in the `tests/` directory.

## Test Options

- For verbose output: `python -m pytest -v`
- To see print statements and other output: `python -m pytest -s`
- Combine flags for more detailed output: `python -m pytest -v -s`

## Running Specific Tests

- All tool tests: `python -m pytest tests/tools/`
- Specific tool test: `python -m pytest tests/tools/test_<tool_name>.py`
- Tool manager test: `python -m pytest tests/test_tool_manager.py`
- All adapter tests: `python -m pytest tests/adapters/`
- Specific adapter test: `python -m pytest tests/adapters/test_<adapter_name>.py`
- Agent gateway test: `python -m pytest tests/test_agent_gateway.py`

## Continuous Integration

Consider setting up a CI/CD pipeline that runs these tests automatically on each commit or pull request. This will help catch any regressions early in the development process.

## Test Coverage

To generate a test coverage report:

1. Install the coverage tool: `pip install coverage`
2. Run tests with coverage: `coverage run -m pytest`
3. Generate a report: `coverage report`
4. For a detailed HTML report: `coverage html`

Aim for high test coverage to ensure the reliability and stability of the AI Agent Gateway project.
