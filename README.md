# Video Size Calculator 🎥

A Python utility to calculate the total size of video files referenced in JSON files.

## Setup 🛠️

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install .
```

## Usage 📝

The script supports processing single or multiple JSON files using glob patterns:

```bash
# Process a single file
python src/util/calculate_size.py data.json

# Process all JSON files in a directory
python src/util/calculate_size.py "data/*.json"

# Process JSON files in multiple directories
python src/util/calculate_size.py "data/**/*.json"
```

## Input Format 📋

The script expects JSON files containing video information in the following format:

```json
[
    {
        "title": "Video Title",
        "url": "https://example.com/video.mp4"
    }
]
```

## Output 📊

The script will display:
- Individual file sizes for each video
- Total size per JSON file
- Combined statistics when processing multiple files

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
