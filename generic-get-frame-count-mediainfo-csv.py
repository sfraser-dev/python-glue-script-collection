import os
import pathlib
import subprocess

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

            # Get the frame count using MediaInfo
            media_info_command = ['MediaInfo.exe', '-f', '--Inform=Video;%FrameCount%', file_path]
            proc = subprocess.Popen(media_info_command, stdout=subprocess.PIPE)
            frame_count_output, _ = proc.communicate()
            frame_count = int(frame_count_output.decode().strip())

            logger.info(f"{file_count}, {frame_count}, {file_path}")

logging.info(f"Total MP4 files: {file_count}")

