import asyncio
import glob
import json
import os
import sys
import subprocess
from typing import Dict, List, Optional, Tuple

import aiohttp
from tqdm import tqdm


def human_readable_size(size_bytes: float) -> str:
    """Convert bytes to human readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def size_to_bytes(size_str: str) -> int:
    """Convert human readable size to bytes."""
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    size_str = size_str.strip().upper()
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            return int(float(size_str[: -len(unit)]) * multiplier)
    return int(float(size_str))


async def get_file_size(session: aiohttp.ClientSession, url: str) -> int:
    """Get file size using HEAD request asynchronously."""
    try:
        async with session.head(url, allow_redirects=True) as response:
            response.raise_for_status()
            return int(response.headers.get("content-length", 0))
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return 0


async def download_file(
    session: aiohttp.ClientSession,
    url: str,
    output_path: str,
    pbar: tqdm,
) -> bool:
    """Download file using aiohttp with progress bar."""
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            pbar.total = total_size
            pbar.set_description(os.path.basename(output_path))

            with open(output_path, "wb") as f:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
                    pbar.update(len(chunk))
        return True
    except (aiohttp.ClientError, OSError) as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        return False


async def get_video_sizes(
    session: aiohttp.ClientSession,
    videos: List[Dict],
) -> List[Tuple[Dict, int]]:
    """Get sizes for all videos."""
    tasks = []
    for video in videos:
        if url := video.get("url"):
            tasks.append(get_file_size(session, url))
        else:
            tasks.append(asyncio.sleep(0))

    sizes = await asyncio.gather(*tasks)
    return [(video, size) for video, size in zip(videos, sizes) if video.get("url")]


def select_videos_for_download(
    videos_with_sizes: List[Tuple[Dict, int]],
    max_size_mb: int,
) -> List[Tuple[Dict, int]]:
    """Select videos to download within size limit."""
    max_size_bytes = max_size_mb * 1024 * 1024
    total_size = 0
    selected = []

    # Sort by size (smallest first)
    sorted_videos = sorted(videos_with_sizes, key=lambda x: x[1])

    for video, size in sorted_videos:
        if total_size + size <= max_size_bytes:
            selected.append((video, size))
            total_size += size
        else:
            break

    return selected


async def process_json_file(
    json_path: str,
    output_dir: Optional[str] = None,
    videos_with_sizes: Optional[List[Tuple[Dict, int]]] = None,
) -> Dict[str, int]:
    """Process a single JSON file, either calculating sizes or downloading files."""
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
        if output_dir:
            # Download mode
            os.makedirs(output_dir, exist_ok=True)
            if videos_with_sizes is None:
                videos_with_sizes = await get_video_sizes(session, data)

            # Download files in parallel
            download_tasks = []
            with tqdm(total=len(videos_with_sizes), desc="Downloading") as pbar:
                for video, size in videos_with_sizes:
                    title = video.get("title", "Unknown")
                    safe_title = "".join(
                        c for c in title if c.isalnum() or c in " -_"
                    ).strip()
                    output_path = os.path.join(output_dir, f"{safe_title}.mp4")
                    download_tasks.append(
                        download_file(session, video["url"], output_path, pbar)
                    )

                results = await asyncio.gather(*download_tasks)
                for (video, size), success in zip(videos_with_sizes, results):
                    title = video.get("title", "Unknown")
                    if success:
                        print(f"Downloaded: {title} ({human_readable_size(size)})")
                    else:
                        print(f"Failed to download: {title}")

        else:
            # Size calculation mode
            tasks = []
            for video in data:
                if url := video.get("url"):
                    tasks.append(get_file_size(session, url))

            sizes = await asyncio.gather(*tasks)

            for video, size in zip(data, sizes):
                if video.get("url"):
                    total_size += size
                    title = video.get("title", "Unknown")
                    print(f"{title}: {human_readable_size(size)}")

    print("-" * 80)
    if not output_dir:
        print(f"Total size for {json_path}: {human_readable_size(total_size)}")
    return {"total_size": total_size, "files_processed": len(data)}


async def process_files(
    file_pattern: str,
    output_dir: Optional[str] = None,
    max_download_mb: Optional[int] = None,
) -> None:
    """Process all JSON files matching the given glob pattern."""
    json_files = glob.glob(file_pattern)
    if not json_files:
        print(f"No files found matching pattern: {file_pattern}")
        return

    total_size = 0
    total_files = 0

    async with aiohttp.ClientSession() as session:
        if output_dir and max_download_mb:
            # First pass: collect all videos and their sizes
            all_videos = []
            for json_file in json_files:
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    all_videos.extend(data)
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"Error reading {json_file}: {e}", file=sys.stderr)
                    continue

            # Get sizes for all videos
            videos_with_sizes = await get_video_sizes(session, all_videos)
            # Select videos within size limit
            selected_videos = select_videos_for_download(
                videos_with_sizes, max_download_mb
            )
            print(
                f"\nSelected {len(selected_videos)} videos within {max_download_mb}MB limit"
            )

            # Second pass: download selected videos
            for json_file in json_files:
                await process_json_file(json_file, output_dir, selected_videos)
        else:
            # Normal processing without size limit
            for json_file in json_files:
                result = await process_json_file(json_file, output_dir)
                total_size += result["total_size"]
                total_files += result["files_processed"]

    if len(json_files) > 1 and not output_dir:
        print("\nSummary:")
        print("-" * 80)
        print(f"Total files processed: {total_files}")
        print(f"Combined size: {human_readable_size(total_size)}")


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Process video metadata JSON files.")
    parser.add_argument(
        "pattern",
        help="Glob pattern for JSON files (e.g., '*.json' or 'data/*.json')",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output directory for downloaded files. If omitted, only sizes will be calculated.",
    )
    parser.add_argument(
        "--max-download",
        "-m",
        type=int,
        help="Maximum download size in megabytes. If specified, only downloads files that fit within this limit.",
    )

    args = parser.parse_args()

    if args.output and not os.path.isdir(args.output):
        try:
            os.makedirs(args.output)
        except OSError as e:
            print(f"Error creating output directory: {e}", file=sys.stderr)
            sys.exit(1)

    asyncio.run(process_files(args.pattern, args.output, args.max_download))


if __name__ == "__main__":
    main()
