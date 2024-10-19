# Makefile

# Ensure that Python and pip are available
PYTHON := python3
PIP := pip3

# Setup virtual environment
venv:
	$(PYTHON) -m venv venv
	. venv/bin/activate && $(PIP) install -r requirements.txt

# Setup DynamoDB
setup-memory-dynamo: venv
	. venv/bin/activate && $(PYTHON) setup/setup_conversations_dynamo.py

# Setup Redis
setup-memory-redis: venv
	. venv/bin/activate && $(PYTHON) setup/setup_conversations_redis.py

# Setup both DynamoDB and Redis
setup-all: setup-memory-dynamo setup-memory-redis

# Clean up
clean:
	rm -rf venv
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

test:
	python -m pytest

.PHONY: venv setup-dynamo setup-redis setup-all clean test

