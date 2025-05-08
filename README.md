# PsTuts VQA Dataset Tools

Tools for processing and analyzing the Photoshop Tutorials Video QA Dataset.

## About the Dataset

PsTuts-VQA is a video question answering dataset on the narrated instructional videos for an image editing software. All the videos and their manual transcripts in English were obtained from the official website of the software. To collect a high-quality question answering dataset, three image editing experts using the software were hired and asked to watch the videos in sequence and generate a question and answer pair at a moment in the video. Each answer is linked to an entity or an option in an existing knowledge base for the software.

The dataset includes:
- 76 videos (5.6 hours in total)
- 17,768 question-answer pairs
- Domain knowledge-base with 1,236 entities and 2,196 options

For more information, visit: https://sites.google.com/view/pstuts-vqa/home

## Features

- Calculate sizes of remote MP4 files from JSON dataset
- Human-readable size formatting
- Total size calculation
- Error handling for inaccessible URLs

## Requirements

- Python 3.8 or higher
- `uv` package manager (recommended) or `pip`

## Installation

Using `uv` (recommended):

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install requests
```

Using `pip`:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install requests
```

## Usage

### Calculate Video Sizes

The `calculate_size.py` script reads a JSON file containing video metadata and calculates the size of each MP4 file:

```bash
python src/util/calculate_size.py path/to/videos.json
```

Example output:
```
File sizes:
--------------------------------------------------------------------------------
Video Title 1: 23.89 MB
Video Title 2: 76.51 MB
...
--------------------------------------------------------------------------------
Total size: 717.56 MB
```

## Project Structure

```
.
├── src/
│   └── util/
│       └── calculate_size.py  # Video size calculation script
├── pyproject.toml            # Project configuration and dependencies
├── README.md                # This file
└── .gitignore              # Git ignore patterns
```

## Development

This project uses:
- `pyproject.toml` for project configuration
- `ruff` for linting and code formatting

## License

This dataset is licensed under Creative Commons Attribution-NonCommercial 4.0 International License.
See: https://creativecommons.org/licenses/by-nc/4.0/legalcode
