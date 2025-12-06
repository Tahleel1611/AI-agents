.PHONY: help install test lint format clean run

# Default target
help:
	@echo "AI-Agents Makefile Commands:"
	@echo "  make install      - Install all dependencies"
	@echo "  make test         - Run tests with pytest"
	@echo "  make lint         - Run linting (ruff + flake8)"
	@echo "  make format       - Format code (black + ruff)"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make run          - Run SmartTravel AI (interactive mode)"
	@echo "  make run-query    - Run SmartTravel AI with query (set QUERY variable)"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

# Run tests
test:
	@echo "Running tests..."
	pytest -v --cov=. --cov-report=term-missing
	@echo "✓ Tests complete"

# Lint code
lint:
	@echo "Running linters..."
	ruff check .
	flake8 . --max-line-length=120 --exclude=.venv,__pycache__
	mypy --ignore-missing-imports .
	@echo "✓ Linting complete"

# Format code
format:
	@echo "Formatting code..."
	black . --line-length=100
	ruff check --fix .
	@echo "✓ Code formatted"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleanup complete"

# Run SmartTravel AI in interactive mode
run:
	@echo "Starting SmartTravel AI (interactive mode)..."
	python main.py --interactive

# Run SmartTravel AI with a query
run-query:
	@if [ -z "$(QUERY)" ]; then \
		echo "Error: Please provide a QUERY variable"; \
		echo "Example: make run-query QUERY='Plan a trip to Paris'"; \
		exit 1; \
	fi
	python main.py "$(QUERY)"

# Run specific agent module
run-my-agent:
	@echo "Running my_agent..."
	cd my_agent && python agent.py
