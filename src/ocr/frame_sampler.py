import cv2
import os
import numpy as np
from pathlib import Path


def sample_frames(video_path, output_dir=None, fps=1):
    """
    Sample frames from a video at specified FPS using OpenCV.

    Args:
        video_path (str): Path to the video file
        output_dir (str, optional): Directory to save frames. If None, frames are not saved.
        fps (int): Frames per second to sample

    Returns:
        list: List of frames as numpy arrays in RGB format
    """
    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return []

    # Get video properties
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate frame interval
    frame_interval = int(video_fps / fps)

    frames = []
    frame_number = 0
    empty_frames = 0
    max_empty_frames = 10  # Maximum number of consecutive empty frames to tolerate

    while True:
        ret, frame = cap.read()
        if not ret:
            empty_frames += 1
            if empty_frames >= max_empty_frames:
                print(
                    f"Warning: Found {max_empty_frames} consecutive empty frames at frame {frame_number}, stopping"
                )
                break
            continue

        # Reset empty frame counter when we get a valid frame
        empty_frames = 0

        if frame_number % frame_interval == 0:
            # Check if frame is empty (all zeros)
            if np.all(frame == 0):
                print(
                    f"Warning: Empty frame detected at frame {frame_number}, skipping"
                )
                continue

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)

            # Save frame if output directory is specified
            if output_dir:
                frame_path = os.path.join(output_dir, f"frame_{frame_number:06d}.jpg")
                cv2.imwrite(frame_path, frame)

        frame_number += 1

    cap.release()
    return frames


def process_video_directory(input_dir, output_dir, fps=1):
    """
    Process all videos in a directory.

    Args:
        input_dir (str): Directory containing video files
        output_dir (str): Directory to save frames
        fps (int): Frames per second to sample
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Process each video file
    for video_file in input_path.glob("*.mp4"):
        video_name = video_file.stem
        video_output_dir = output_path / video_name

        print(f"Processing {video_name}...")
        frames = sample_frames(str(video_file), str(video_output_dir), fps)
        print(f"Sampled {len(frames)} frames from {video_name}")


if __name__ == "__main__":
    # Example usage
    input_dir = "../../data/test"
    output_dir = "sampled_frames"
    process_video_directory(input_dir, output_dir, fps=1)
