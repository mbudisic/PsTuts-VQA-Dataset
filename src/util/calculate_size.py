import json
import requests
from pathlib import Path
from typing import Dict, List
import sys


def human_readable_size(size_bytes: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_file_size(url: str) -> int:
    """Get file size using HEAD request."""
    try:
        response = requests.head(url, allow_redirects=True)
        response.raise_for_status()
        return int(response.headers.get("content-length", 0))
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return 0


def calculate_sizes(json_path: str) -> None:
    """Calculate sizes of all MP4 files in the JSON."""
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading JSON file: {e}", file=sys.stderr)
        return

    total_size = 0
    print("\nFile sizes:")
    print("-" * 80)

    for video in data:
        url = video.get("url")
        if not url:
            continue

        size = get_file_size(url)
        total_size += size

        print(f"{video.get('title', 'Unknown')}: {human_readable_size(size)}")

    print("-" * 80)
    print(f"Total size: {human_readable_size(total_size)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_size.py <path_to_json>")
        sys.exit(1)

    calculate_sizes(sys.argv[1])
