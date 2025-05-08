import asyncio
import glob
import json
import sys
from typing import Dict

import aiohttp
from pathlib import Path
from typing import List


def human_readable_size(size_bytes: float) -> str:
    """Convert bytes to human readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


async def get_file_size(session: aiohttp.ClientSession, url: str) -> int:
    """Get file size using HEAD request asynchronously."""
    try:
        async with session.head(url, allow_redirects=True) as response:
            response.raise_for_status()
            return int(response.headers.get("content-length", 0))
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return 0


async def calculate_sizes(json_path: str) -> Dict[str, int]:
    """Calculate sizes of all MP4 files in the JSON using async requests.

    Returns:
        Dict containing total size and number of files processed
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading JSON file {json_path}: {e}", file=sys.stderr)
        return {"total_size": 0, "files_processed": 0}

    total_size = 0
    print(f"\nProcessing {json_path}:")
    print("-" * 80)

    async with aiohttp.ClientSession() as session:
        # Create tasks for all URLs
        tasks = []
        for video in data:
            url = video.get("url")
            if url:
                tasks.append(get_file_size(session, url))

        # Wait for all requests to complete
        sizes = await asyncio.gather(*tasks)

        # Process results
        for video, size in zip(data, sizes):
            if video.get("url"):  # Only process videos that had URLs
                total_size += size
                title = video.get("title", "Unknown")
                print(f"{title}: {human_readable_size(size)}")

    print("-" * 80)
    print(f"Total size for {json_path}: {human_readable_size(total_size)}")
    return {"total_size": total_size, "files_processed": len(data)}


async def process_files(file_pattern: str) -> None:
    """Process all JSON files matching the given glob pattern."""
    json_files = glob.glob(file_pattern)
    if not json_files:
        print(f"No files found matching pattern: {file_pattern}")
        return

    total_size = 0
    total_files = 0

    for json_file in json_files:
        result = await calculate_sizes(json_file)
        total_size += result["total_size"]
        total_files += result["files_processed"]

    if len(json_files) > 1:
        print("\nSummary:")
        print("-" * 80)
        print(f"Total files processed: {total_files}")
        print(f"Combined size: {human_readable_size(total_size)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_size.py <glob_pattern>")
        print("Example: python calculate_size.py 'data/*.json'")
        sys.exit(1)

    asyncio.run(process_files(sys.argv[1]))
