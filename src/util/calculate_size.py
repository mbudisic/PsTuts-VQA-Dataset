import json
import aiohttp
import asyncio
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


async def get_file_size(session: aiohttp.ClientSession, url: str) -> int:
    """Get file size using HEAD request asynchronously."""
    try:
        async with session.head(url, allow_redirects=True) as response:
            response.raise_for_status()
            return int(response.headers.get("content-length", 0))
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return 0


async def calculate_sizes(json_path: str) -> None:
    """Calculate sizes of all MP4 files in the JSON using async requests."""
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading JSON file: {e}", file=sys.stderr)
        return

    total_size = 0
    print("\nFile sizes:")
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
                print(f"{video.get('title', 'Unknown')}: {human_readable_size(size)}")

    print("-" * 80)
    print(f"Total size: {human_readable_size(total_size)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_size.py <path_to_json>")
        sys.exit(1)

    asyncio.run(calculate_sizes(sys.argv[1]))
