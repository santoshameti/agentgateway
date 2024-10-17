# Contributing to AI Agent Gateway

We welcome contributions to the AI Agent Gateway project! This document outlines the process for contributing to the project and guidelines to follow.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```
   git clone https://github.com/your-username/ai-agent-gateway.git
   cd ai-agent-gateway
   ```
3. Create a new branch for your feature or bug fix:
   ```
   git checkout -b feature-or-fix-name
   ```

## Development Environment

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Making Changes

1. Make your changes in your feature branch.
2. Write or update tests for your changes.
3. Run the tests to ensure they pass:
   ```
   python -m pytest
   ```
4. Update the documentation if necessary.

## Commit Guidelines

- Use clear and descriptive commit messages.
- Reference issue numbers in your commit messages if applicable.
- Make small, focused commits rather than large, sweeping changes.

## Submitting a Pull Request

1. Push your changes to your fork on GitHub:
   ```
   git push origin feature-or-fix-name
   ```
2. Go to the original AI Agent Gateway repository on GitHub.
3. Click the "New Pull Request" button.
4. Select your fork and the feature branch containing your changes.
5. Provide a clear title and description for your pull request.
6. Submit the pull request for review.

## Code Style

- Follow PEP 8 guidelines for Python code.
- Use type hints where appropriate.
- Write clear and concise docstrings for classes and methods.

## Testing

- Write unit tests for new features or bug fixes.
- Ensure all tests pass before submitting a pull request.
- Aim for high test coverage for new code.

## Documentation

- Update the README.md file if your changes affect the project setup or usage.
- Update or add docstrings for new or modified classes and methods.
- If adding new features, update the relevant documentation files in the `docs/` directory.

## Review Process

- All submissions require review before being merged.
- Be open to feedback and be willing to make changes to your code.
- Respond promptly to comments on your pull request.

## Licensing

By contributing to AI Agent Gateway, you agree that your contributions will be licensed under the project's MIT License.

Thank you for contributing to the AI Agent Gateway project! Your efforts help make this project better for everyone.
