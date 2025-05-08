# 🛠️ Developer Guide for PsTuts-VQA-Dataset

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/PsTuts-VQA-Dataset.git
cd PsTuts-VQA-Dataset

# Create and activate virtual environment using system Python
/usr/bin/python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

## 📁 Project Structure

```
.
├── src/                    # Source code
│   └── util/              # Utility functions
│       └── fetch.py       # Video fetching utilities
├── data/                  # Dataset files
├── test_videos/          # Test video files
├── pyproject.toml        # Project configuration
└── tests/                # Test files
```

## 🛠️ Development Setup

### Prerequisites
- Python 3.8 or higher
- System Python (recommended: /usr/bin/python3)

### Environment Setup
1. Create virtual environment using system Python:
   ```bash
   /usr/bin/python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Code Quality Tools
- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing

## 🧪 Testing

Run tests using pytest:
```bash
pytest
```

## 📝 Code Style

- Line length: 88 characters (Black default)
- Type hints: Required for all functions
- Docstrings: Required for all public functions

## 🔄 Development Workflow

1. Create a new branch for your feature
2. Make your changes
3. Run tests and linting:
   ```bash
   pytest
   black .
   flake8
   mypy .
   ```
4. Submit a pull request

## 🎯 Key Components

### Video Fetching (`src/util/fetch.py`)
- Asynchronous video downloading
- Progress tracking with tqdm
- Size calculation and management
- Parallel downloads using curl

### Dataset Structure
- JSON-based metadata
- Organized video storage
- Size-aware download management

## 🚨 Common Issues

1. **Python Environment Issues**
   - Use system Python (/usr/bin/python3) for virtual environment creation
   - Ensure PYTHONPATH is set correctly when running scripts

2. **Type Checking Errors**
   - Ensure all functions have proper type hints
   - Run `mypy .` to check types

3. **Linting Errors**
   - Run `black .` to format code
   - Run `flake8` to check for style issues

## 📚 Additional Resources

- [Python Documentation](https://docs.python.org/3/)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [Pytest Documentation](https://docs.pytest.org/)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details. 