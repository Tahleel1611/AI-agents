# Contributing to AI-Agents

Thank you for your interest in contributing to AI-Agents! This document provides guidelines and information for contributors.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment details (Python version, OS, etc.)

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:

- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you may have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** for any new functionality
4. **Run the test suite** to ensure nothing is broken
5. **Update documentation** if needed
6. **Submit a pull request** with a clear description

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/AI-agents.git
   cd AI-agents
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install development dependencies:
   ```bash
   pip install pytest black flake8 mypy
   ```

## Coding Standards

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions, classes, and modules
- Keep functions focused and concise
- Use meaningful variable and function names

## Code Formatting

We use `black` for code formatting and `flake8` for linting:

```bash
# Format code
black .

# Check for linting issues
flake8 .
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest smarttravel/tests/test_agents.py -v
```

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Keep the first line under 72 characters
- Reference issue numbers when applicable (e.g., "Fix #123")

## Questions?

Feel free to open an issue for any questions or discussions.

Thank you for contributing! 🎉
