import os
import subprocess
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('script.log')
logger.addHandler(handler)

file_count = 0

# Find all MP4 files in the current directory and its subdirectories
for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.mp4'):
            file_path = os.path.join(root, file)
            file_count += 1

            # Convert the MP4 file to MP3 using FFmpeg
            output_file_path = file_path.replace('.mp4', '.mp3')
            ffmpeg_command = ['ffmpeg', '-y', '-i', file_path, '-b:a', '192k', '-vn', output_file_path]
            subprocess.call(ffmpeg_command)

            logger.info(f"{file_count}, {file_path}")

logging.info(f"Total MP4 files processed: {file_count}")

