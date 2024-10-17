# Installation Guide

This guide will walk you through the process of installing the AI Agent Gateway on your system.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7 or higher
- pip (Python package installer)
- git (version control system)

## Step 1: Clone the Repository

First, clone the AI Agent Gateway repository to your local machine:

```bash
git clone https://github.com/yourusername/ai-agent-gateway.git
cd ai-agent-gateway
```

## Step 2: Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies for your project. Here's how to set it up:

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

## Step 3: Install Dependencies

With the virtual environment activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

This command will install all the necessary packages listed in the `requirements.txt` file.

## Step 4: Verify Installation

To verify that the installation was successful, you can run the tests:

```bash
python -m pytest
```

If all tests pass, you've successfully installed the AI Agent Gateway.

## Next Steps

Now that you have installed the AI Agent Gateway, you can proceed to:

1. [Configure your environment](configuration.md)
2. [Quick start guide](quick-start.md)

If you encounter any issues during installation, please check our [troubleshooting guide](../troubleshooting.md) or reach out to our community support channels.
