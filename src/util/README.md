# Util Package

A collection of utility functions and helpers for the project.

## Installation

```bash
pip install -e .
```

## Usage

```python
from util import some_function

# Use the utility functions
```

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## License

MIT License

# Utility Scripts 🛠️

This directory contains utility scripts for managing and processing the dataset.

## Available Scripts

### `calculate_size.py` 📏

Calculates the total size of MP4 files referenced in JSON metadata files.

```bash
python calculate_size.py "*.json"
```

Features:
- Supports glob patterns for processing multiple JSON files
- Shows individual file sizes and total size
- Human-readable size formatting (B, KB, MB, GB, TB)

### `fetch.py` 📥

Downloads MP4 files from URLs specified in JSON metadata files.

```bash
# Calculate sizes only
python fetch.py "*.json"

# Download all files
python fetch.py "*.json" --output videos

# Download files within size limit
python fetch.py "*.json" --output videos --max-download 200
```

Features:
- Parallel downloads for faster processing
- Progress bar showing download status
- Size limit option to stay within storage constraints
- Shows download plan before starting
- Verifies downloaded file sizes
- Lists full filepaths of downloaded files

## Environment Setup 🚀

1. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install -e .
```

## Notes 📝

- Downloaded MP4 files are ignored by Git (see `.gitignore`)
- All scripts support glob patterns for processing multiple JSON files
- Scripts use UTF-8 encoding for file operations
