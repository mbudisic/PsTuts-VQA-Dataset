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
) -> Tuple[bool, int]:
    """Download file using aiohttp with progress bar."""
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            pbar.total = total_size
            pbar.set_description(os.path.basename(output_path))

            with open(output_path, "wb") as f:
                downloaded_size = 0
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    pbar.update(len(chunk))
        return True, downloaded_size
    except (aiohttp.ClientError, OSError) as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        return False, 0


def read_json_file(json_path: str) -> List[Dict]:
    """Read and validate a JSON file containing video metadata."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading {json_path}: {e}", file=sys.stderr)
        return []


def get_safe_filename(title: str) -> str:
    """Convert video title to safe filename."""
    return "".join(c for c in title if c.isalnum() or c in " -_").strip()


def get_subfolder_path(
    output_dir: str,
    source_json: str,
) -> str:
    """Get subfolder path based on JSON filename."""
    json_name = os.path.splitext(os.path.basename(source_json))[0]
    subfolder = os.path.join(output_dir, json_name)
    os.makedirs(subfolder, exist_ok=True)
    return subfolder


def get_output_path(
    video: Dict,
    output_dir: str,
    json_to_videos: Dict[str, List[Dict]],
) -> str:
    """Generate output path for video file."""
    safe_title = get_safe_filename(video.get("title", "Unknown"))

    # Find source JSON file
    source_json = next(
        (json_file for json_file, videos in json_to_videos.items() if video in videos),
        None,
    )

    if not source_json:
        return os.path.join(output_dir, f"{safe_title}.mp4")

    subfolder = get_subfolder_path(output_dir, source_json)
    return os.path.join(subfolder, f"{safe_title}.mp4")


def print_video_info(
    videos: List[Tuple[Dict, int]],
    title: str = "Video Information",
    quiet: bool = False,
) -> None:
    """Print information about videos."""
    if quiet:
        return

    print(f"\n{title}:")
    print("-" * 80)
    total_size = sum(size for _, size in videos)
    print(f"Total files: {len(videos)}")
    print(f"Total size: {human_readable_size(total_size)}")
    print("\nFiles:")
    for video, size in videos:
        title = video.get("title", "Unknown")
        print(f"- {title} ({human_readable_size(size)})")
    print("-" * 80)


async def get_video_info(
    session: aiohttp.ClientSession,
    json_files: List[str],
) -> Tuple[List[Dict], Dict[str, List[Dict]]]:
    """Read all JSON files and get video information."""
    all_videos = []
    json_to_videos = {}

    for json_file in json_files:
        data = read_json_file(json_file)
        if data:
            all_videos.extend(data)
            json_to_videos[json_file] = data

    return all_videos, json_to_videos


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


async def download_videos(
    session: aiohttp.ClientSession,
    videos_to_download: List[Tuple[Dict, int]],
    output_dir: str,
    json_to_videos: Dict[str, List[Dict]],
) -> None:
    """Download selected videos."""
    download_tasks = []
    file_paths = []

    with tqdm(total=len(videos_to_download), desc="Downloading") as pbar:
        for video, _ in videos_to_download:
            output_path = get_output_path(video, output_dir, json_to_videos)
            file_paths.append(output_path)
            download_tasks.append(
                download_file(session, video["url"], output_path, pbar)
            )

        results = await asyncio.gather(*download_tasks)

        for (video, _), (success, downloaded_size), filepath in zip(
            videos_to_download, results, file_paths
        ):
            title = video.get("title", "Unknown")
            if success:
                print(
                    f"✓ {title}\n"
                    f"  Path: {filepath}\n"
                    f"  Size: {human_readable_size(downloaded_size)}"
                )
            else:
                print(f"✗ Failed to download: {title}")
            print()


def generate_curl_command(
    videos: List[Tuple[Dict, int]],
    output_dir: str,
    json_to_videos: Dict[str, List[Dict]],
) -> str:
    """Generate curl command for downloading videos in parallel."""
    # Create curl command
    curl_cmd = [
        "curl --progress-bar --create-dirs --parallel --parallel-immediate --parallel-max 5  \\"
    ]
    for video, _ in videos:
        output_path = get_output_path(video, output_dir, json_to_videos)
        url = video.get("url", "")
        if url:
            curl_cmd.append(f"  -o '{output_path}' '{url}' \\")
    curl_cmd[-1] = curl_cmd[-1].rstrip(
        " \\"
    )  # Remove trailing backslash from last line

    # Return the command
    return "\n".join(curl_cmd)


async def process_files(
    file_pattern: str,
    output_dir: Optional[str] = None,
    max_download_mb: Optional[int] = None,
    use_curl: bool = False,
    quiet: bool = False,
) -> None:
    """Process all JSON files matching the given glob pattern."""
    json_files = glob.glob(file_pattern)
    if not json_files:
        if not quiet:
            print(f"No files found matching pattern: {file_pattern}")
        return

    async with aiohttp.ClientSession() as session:
        # Step 1: Read all JSON files and get video information
        all_videos, json_to_videos = await get_video_info(session, json_files)
        if not all_videos:
            if not quiet:
                print("No videos found in JSON files")
            return

        # Step 2: Get sizes for all videos
        videos_with_sizes = await get_video_sizes(session, all_videos)

        if not output_dir:
            # Size calculation mode
            print_video_info(videos_with_sizes, "Size Summary", quiet)
            return

        # Step 3: Select videos to download
        if max_download_mb:
            selected_videos = select_videos_for_download(
                videos_with_sizes, max_download_mb
            )
        else:
            selected_videos = videos_with_sizes

        if use_curl:
            # Generate and print curl command
            print(generate_curl_command(selected_videos, output_dir, json_to_videos))
        else:
            # Show download plan and download files
            print_video_info(selected_videos, "Download Plan", quiet)
            await download_videos(session, selected_videos, output_dir, json_to_videos)


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="""
Video metadata processor with three modes of operation:

1. Size Calculation Mode (default):
   Run without --output to calculate sizes of videos referenced in JSON files.
   Example: python fetch.py "*.json"

2. Full Download Mode:
   Download all videos to specified output directory.
   Example: python fetch.py "*.json" --output videos

3. Limited Download Mode:
   Download videos up to specified size limit.
   Example: python fetch.py "*.json" --output videos --max-download 200

4. Curl Command Mode:
   Generate curl commands for downloading videos.
   Example: python fetch.py "*.json" --output videos --curl > download.sh

All modes support glob patterns for processing multiple JSON files.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
    parser.add_argument(
        "--curl",
        action="store_true",
        help="Generate curl command instead of downloading files directly.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress all output except the curl command when --curl is used.",
    )

    args = parser.parse_args()

    if args.output and not os.path.isdir(args.output):
        try:
            os.makedirs(args.output)
        except OSError as e:
            print(f"Error creating output directory: {e}", file=sys.stderr)
            sys.exit(1)

    asyncio.run(
        process_files(
            args.pattern,
            args.output,
            args.max_download,
            args.curl,
            args.quiet,
        )
    )


if __name__ == "__main__":
    main()
