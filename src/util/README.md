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

### `fetch.py` 📥

A versatile script for processing video metadata JSON files with three modes of operation:

1. **Size Calculation Mode** (default)
   ```bash
   python fetch.py "*.json"
   ```
   - Calculates sizes of videos referenced in JSON files
   - Shows individual file sizes and total size
   - Human-readable size formatting (B, KB, MB, GB, TB)

2. **Full Download Mode**
   ```bash
   python fetch.py "*.json" --output videos
   ```
   - Downloads all videos to specified output directory
   - Parallel downloads for faster processing
   - Progress bar showing download status
   - Verifies downloaded file sizes

3. **Limited Download Mode**
   ```bash
   python fetch.py "*.json" --output videos --max-download 200
   ```
   - Downloads videos up to specified size limit (in MB)
   - Shows download plan before starting
   - Lists full filepaths of downloaded files
   - Verifies downloaded file sizes

Common Features:
- Supports glob patterns for processing multiple JSON files
- UTF-8 encoding for file operations
- Progress tracking and status reporting
- Error handling and reporting

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
- For more detailed help, run: `python fetch.py --help`
