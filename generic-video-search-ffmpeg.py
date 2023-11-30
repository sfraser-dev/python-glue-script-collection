import os
import subprocess
import logging

# Specify the top-level folder containing the videos to be converted
vid_originals_folder = "F:\\VIDEO_FIX\\mpegToH264"

# Check if the folder exists
if not os.path.exists(vid_originals_folder):
    logging.error(f"Error: folder '{vid_originals_folder}' doesn't exist. Please point to the folder containing the videos to be converted.")
    exit(1)

# Find all MPG files in the specified folder and its subdirectories
vid_files = []
for root, _, files in os.walk(vid_originals_folder):
    for file in files:
        if file.endswith('.mpg'):
            vid_files.append(os.path.join(root, file))

logging.info(f"Found {len(vid_files)} MPG files to convert")

# Convert each MPG file to MP4 using FFmpeg
for vid_file in vid_files:
    original_file_path = os.path.abspath(vid_file)
    converted_file_path = original_file_path.replace('.mpg', '.mp4')
    ffmpeg_command = ['ffmpeg', '-i', original_file_path, '-f', 'mp4', converted_file_path]
    subprocess.call(ffmpeg_command)

    logging.info(f"Converted {original_file_path} to {converted_file_path}")

