PYTHON ?= python3
SRC_DIR := src
PACKAGE_NAME := nodus
VENV_DIR := venv
export PYTHONPATH := $(shell pwd)/$(SRC_DIR)

.PHONY: help setup-venv install run-server run-mock-server run-client clean lint test proto-gen kill

all: help

setup-venv:
	@echo "Setting up virtual environment..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created at $(VENV_DIR)"
	@echo "To activate, run: source $(VENV_DIR)/bin/activate"

install:
	@echo "Installing dependencies..."
	@. $(VENV_DIR)/bin/activate && pip install -r requirements.txt
	@echo "Dependencies installed."

run-server:
	@echo "Starting the Nodus server..."
	@. $(VENV_DIR)/bin/activate && $(PYTHON) -m $(PACKAGE_NAME).core.interfaces.server &

run-mock-server:
	@echo "Starting the Nodus mock server..."
	@. $(VENV_DIR)/bin/activate && $(PYTHON) -m $(PACKAGE_NAME).core.interfaces.server --mock &

run-client:
	@echo "Running the Nodus test client..."
	@. $(VENV_DIR)/bin/activate && $(PYTHON) -m $(PACKAGE_NAME).core.interfaces.client

clean:
	@echo "Cleaning up Python artifacts..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Cleanup complete."

lint:
	@echo "Running linter..."
	@. $(VENV_DIR)/bin/activate && ruff check .

test:
	@echo "Running tests..."
	@. $(VENV_DIR)/bin/activate && pytest

proto-gen:
	@echo "Generating Spounge SDK..."
	@. $(VENV_DIR)/bin/activate && $(PYTHON) scripts/generate_spounge_sdk.py

kill:
	@echo "Killing all running servers..."
	@-pkill -f "python -m nodus.core.interfaces.server"

help:
	@echo "--------------------------------------------------"
	@echo " Nodus"
	@echo "--------------------------------------------------"
	@echo "Available commands:"
	@echo " make setup-venv - Creates a Python virtual environment."
	@echo " make install - Installs dependencies from requirements.txt."
	@echo " make run-server - Starts the application server."
	@echo " make run-mock-server - Starts the mock application server."
	@echo " make run-client - Runs the test client."
	@echo " make lint - Runs the linter."
	@echo " make test - Runs the tests."
	@echo " make proto-gen - Generates the Spounge SDK."
	@echo " make kill - Kills all running servers."
	@echo " make clean - Removes Python cache files."
	@echo " make help - Shows this help message."
	@echo "--------------------------------------------------"