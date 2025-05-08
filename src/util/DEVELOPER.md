# 🔧 Extending Video Fetching Utilities

## 📦 Module Overview

The `fetch.py` module provides a robust framework for downloading and managing video datasets. It's built with extensibility in mind, using modern Python features like async/await and type hints.

## 🎯 Core Components

### 1. Video Information Management
```python
async def get_video_info(session: aiohttp.ClientSession, json_files: List[str]) -> Tuple[List[Dict], Dict[str, List[Dict]]]
```
- Handles JSON metadata parsing
- Maintains mapping between JSON files and videos
- Returns tuple of (all_videos, json_to_videos_mapping)

### 2. Download Management
```python
async def download_file(session: aiohttp.ClientSession, url: str, output_path: str, pbar: tqdm) -> Tuple[bool, int]
```
- Asynchronous file downloading
- Progress tracking with tqdm
- Returns (success_status, downloaded_size)

### 3. Size Management
```python
def select_videos_for_download(videos_with_sizes: List[Tuple[Dict, int]], max_size_mb: int) -> List[Tuple[Dict, int]]
```
- Smart video selection based on size constraints
- Prioritizes smaller videos when space is limited

## 🔄 Extension Points

### 1. Adding New Download Methods

To add a new download method:

```python
async def custom_download_method(
    session: aiohttp.ClientSession,
    url: str,
    output_path: str,
    pbar: tqdm,
    **kwargs
) -> Tuple[bool, int]:
    """Custom download implementation.
    
    Args:
        session: aiohttp session
        url: Video URL
        output_path: Output file path
        pbar: Progress bar instance
        **kwargs: Additional parameters
        
    Returns:
        Tuple of (success_status, downloaded_size)
    """
    # Your implementation here
    pass
```

### 2. Custom Video Selection Logic

```python
def custom_video_selector(
    videos_with_sizes: List[Tuple[Dict, int]],
    selection_criteria: Dict
) -> List[Tuple[Dict, int]]:
    """Custom video selection logic.
    
    Args:
        videos_with_sizes: List of (video_dict, size) tuples
        selection_criteria: Custom selection parameters
        
    Returns:
        Selected videos with sizes
    """
    # Your implementation here
    pass
```

### 3. Adding New Metadata Processing

```python
async def process_custom_metadata(
    session: aiohttp.ClientSession,
    metadata_file: str
) -> List[Dict]:
    """Process custom metadata format.
    
    Args:
        session: aiohttp session
        metadata_file: Path to metadata file
        
    Returns:
        List of processed video metadata
    """
    # Your implementation here
    pass
```

## 🛠️ Best Practices

1. **Type Hints**
   - Always use type hints for function parameters and return values
   - Use `Optional[]` for nullable parameters
   - Use `Dict[str, Any]` for flexible dictionary types

2. **Error Handling**
   - Use specific exception types
   - Include meaningful error messages
   - Handle network errors gracefully

3. **Async Patterns**
   - Use `async with` for resource management
   - Implement proper cleanup in error cases
   - Use `asyncio.gather()` for parallel operations

4. **Progress Tracking**
   - Use tqdm for consistent progress reporting
   - Update progress bars atomically
   - Handle cancellation gracefully

## 🧪 Testing Extensions

1. Create test file in `tests/util/test_fetch.py`:
```python
import pytest
from src.util.fetch import YourNewFunction

@pytest.mark.asyncio
async def test_your_new_function():
    # Test implementation
    pass
```

2. Mock external dependencies:
```python
@pytest.fixture
def mock_session():
    # Mock aiohttp session
    pass
```

## 📚 API Reference

### Key Functions

- `get_file_size()`: Get remote file size
- `download_file()`: Download single file
- `process_files()`: Main processing function
- `generate_curl_command()`: Generate curl download commands

### Common Types

```python
from typing import Dict, List, Optional, Tuple

VideoDict = Dict[str, Any]
VideoWithSize = Tuple[VideoDict, int]
```

## 🚨 Common Pitfalls

1. **Environment Setup**
   - Use system Python (/usr/bin/python3) for virtual environment
   - Set PYTHONPATH correctly when running scripts

2. **Memory Management**
   - Use generators for large file processing
   - Implement proper cleanup in async context
   - Monitor memory usage during downloads

3. **Network Handling**
   - Implement retry logic for failed downloads
   - Handle rate limiting
   - Use connection pooling

4. **File System**
   - Check disk space before downloads
   - Handle path encoding issues
   - Implement proper file locking

## 🔍 Debugging Tips

1. Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. Use async debugger:
```python
import asyncio
asyncio.get_event_loop().set_debug(True)
```

3. Monitor network:
```python
import aiohttp
aiohttp.TRACE = True
```

4. Environment Variables:
```bash
# Set Python path correctly
export PYTHONPATH=src

# Run script with debug output
PYTHONPATH=src python src/util/fetch.py "*.json" --output data --curl 2>&1 | tee output.log
``` 