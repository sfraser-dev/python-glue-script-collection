import os
import subprocess
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('script.log')
logger.addHandler(handler)

file_count = 0

# Find all M4V files in the current directory and its subdirectories
for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.m4v'):
            file_path = os.path.join(root, file)
            file_count += 1

            # Get video duration using MediaInfo CLI
            media_info_command = ['MediaInfo.exe', '-f', '--Inform=Video;%Duration%', file_path]
            proc = subprocess.Popen(media_info_command, stdout=subprocess.PIPE)
            media_info_output, _ = proc.communicate()
            media_info_duration_str = media_info_output.decode().strip()
            media_info_duration = int(media_info_duration_str) / 1000

            # Get video duration using FFprobe
            ffprobe_command = ['ffprobe', '-v', 'quiet', '-show_format', file_path]
            proc = subprocess.Popen(ffprobe_command, stdout=subprocess.PIPE)
            ffprobe_output, _ = proc.communicate()
            ffprobe_lines = ffprobe_output.decode().strip().split('\n')

            for line in ffprobe_lines:
                if "duration" in line:
                    duration_key, duration_value = line.split('=')
                    ffprobe_duration = float(duration_value)

            # Log the video durations
            logger.info(f"{file_count}, {media_info_duration}, {ffprobe_duration}, {file_path}")

logging.info(f"Total M4V files processed: {file_count}")

