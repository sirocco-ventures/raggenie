# Define variables
POETRY = poetry
PYTHON = $(POETRY) run python
POETRY_VENV = .venv
PROJECT_DIR=./app

# Specify the directories or files to spell check
SPELLCHECK_FILES := **/*.py


# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install       Install dependencies"


# Install dependencies
.PHONY: install
install:
	$(POETRY) install

# Spellcheck target
.PHONY: spellcheck
spellcheck:
	- codespell $(shell find ./app -name "*.py")

# lint check
.PHONY: lint
lint:
	@echo "Running flake8..."
	flake8 $(PROJECT_DIR)