PYTHON ?= python3
SRC_DIR := src
PACKAGE_NAME := nodus
export PYTHONPATH := $(shell pwd)/$(SRC_DIR)

.PHONY: help run-server run-client clean

all: help

run-server:
	@echo "Starting the Nodus server..."
	@$(PYTHON) -m $(PACKAGE_NAME).core.interfaces.server

run-client:
	@echo "Running the Nodus test client..."
	@$(PYTHON) -m $(PACKAGE_NAME).core.interfaces.client

clean:
	@echo "Cleaning up Python artifacts..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Cleanup complete."

help:
	@echo "--------------------------------------------------"
	@echo " Nodus"
	@echo "--------------------------------------------------"
	@echo "Available commands:"
	@echo " make run-server - Starts the application server."
	@echo " make run-client - Runs the test client."
	@echo " make clean - Removes Python cache files."
	@echo " make help - Shows this help message."
	@echo "--------------------------------------------------"