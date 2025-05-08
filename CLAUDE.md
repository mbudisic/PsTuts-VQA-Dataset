# Environment Management Guide 🛠️

This document outlines the recommended process for managing the Python environment for this project using `uv`.

## Prerequisites

- Python 3.10 or higher
- `uv` package manager installed

## Environment Setup

1. **Create a new virtual environment**
   ```bash
   # Remove existing environment if any
   rm -rf .venv

   # Create new environment with system Python
   uv venv --python=/usr/bin/python3
   ```

2. **Activate the environment**
   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   uv pip install .
   ```

## Common Issues and Solutions

### ModuleNotFoundError: No module named 'encodings'

If you encounter this error:
1. Deactivate any existing virtual environments:
   ```bash
   deactivate 2>/dev/null || true
   ```
2. Remove the existing virtual environment:
   ```bash
   rm -rf .venv
   ```
3. Create a new environment with the system Python:
   ```bash
   uv venv --python=/usr/bin/python3
   ```
4. Activate and install dependencies:
   ```bash
   source .venv/bin/activate && uv pip install .
   ```

## Development Workflow

1. Always activate the environment before working:
   ```bash
   source .venv/bin/activate
   ```

2. Install new dependencies:
   ```bash
   uv pip install <package-name>
   ```

3. Update dependencies:
   ```bash
   uv pip install --upgrade .
   ```

## Notes

- The project uses `pyproject.toml` for dependency management
- All dependencies should be added to `pyproject.toml`, not `requirements.txt`
- The virtual environment should be recreated if you encounter any Python-related issues 