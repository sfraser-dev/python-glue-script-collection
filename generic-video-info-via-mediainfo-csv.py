import subprocess
import logging
import os
import pathlib

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('script.log')
logger.addHandler(handler)

file_count = 0

# Find all MPG files in the current directory and its subdirectories
for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.mpg'):
            file_path = os.path.join(root, file)
            file_count += 1

            # Get media info using MediaInfo CLI
            media_info_command = ['MediaInfo.exe', '-f', file_path]
            proc = subprocess.Popen(media_info_command, stdout=subprocess.PIPE)
            media_info_output, _ = proc.communicate()
            media_info_lines = media_info_output.decode().strip().split('\n')

            # Extract relevant media info
            media_duration = None
            media_bitrate = None
            video_format = None
            video_resolution = None
            video_bitrate = None
            video_frame_rate = None
            video_frame_count = None
            video_duration = None

            for line in media_info_lines:
                key, value = line.split(': ')
                if key == 'General;%Duration%':
                    media_duration = int(value) / 1000
                elif key == 'General;%BitRate%':
                    media_bitrate = int(value)
                elif key == 'Video;%Format%':
                    video_format = value
                elif key == 'Video;%Width%':
                    video_width = int(value)
                elif key == 'Video;%Height%':
                    video_height = int(value)
                    video_resolution = f'{video_width}x{video_height}'
                elif key == 'Video;%BitRate%':
                    video_bitrate = int(value)
                elif key == 'Video;%FrameRate%':
                    video_frame_rate = float(value)
                elif key == 'Video;%FrameCount%':
                    video_frame_count = int(value)
                elif key == 'Video;%Duration%':
                    video_duration = int(value) / 1000

            # Log the media info
            logger.info(f"{file_count}, {file_path}, {media_duration}, {media_bitrate}, {video_format}, {video_resolution}, {video_bitrate}, {video_frame_rate}, {video_frame_count}, {video_duration}")

logging.info(f"Total MPG files processed: {file_count}")

