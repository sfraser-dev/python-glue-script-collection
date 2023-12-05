import subprocess
import csv
import os
from pathlib import Path
from datetime import timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize variables
file_count = 0

# Open CSV file for writing media info
csv_file_path = 'generic-video-info-via-mediainfo-csv.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Write header row to CSV
    writer.writerow(['media count', 'media path', 'media name', 'media duration (secs)',
                     'media bitrate (kbps)', 'video format', 'video resolution', 'video bitrate (kbps)',
                     'video frame rate (fps)', 'video frame count', 'video duration (secs)'])

    # Iterate through current directory and subdirectories
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.mp4'):
                file_count += 1

                # Construct file path
                file_path = os.path.join(root, file)

                # Extract media info using MediaInfo CLI
                media_info_output_duration = subprocess.check_output(
                    ["MediaInfo.exe", "-f", "--Inform=General;%Duration%", file_path],
                    universal_newlines=True,
                    shell=True,
                )
                media_duration = float(media_info_output_duration.strip()) / 1000


                media_info_output_bitrate = subprocess.check_output(
                    ['MediaInfo.exe', '-f', '--Inform=General;%BitRate%', file_path],
                    universal_newlines=True,
                    shell=True,
                )
                media_bitrate = int(media_info_output_bitrate.strip())

                media_info_output_format = subprocess.check_output(
                    ['MediaInfo.exe', '-f', '--Inform=Video;%Format%', file_path],
                    universal_newlines=True,
                    shell=True,
                )
                video_format = media_info_output_format.strip()

                media_info_output_width = subprocess.check_output(
                    ['MediaInfo.exe', '-f', '--Inform=Video;%Width%', file_path],
                    universal_newlines=True,
                    shell=True,
                )
                video_width = int(media_info_output_width.strip())

                media_info_output_height = subprocess.check_output(
                    ['MediaInfo.exe', '-f', '--Inform=Video;%Height%', file_path],
                    universal_newlines=True,
                    shell=True,
                )
                video_height = int(media_info_output_height.strip())

                video_resolution = f'{video_width}x{video_height}'

                media_info_output_bitrate_video = subprocess.check_output([
                    'MediaInfo.exe', '-f', '--Inform=Video;%BitRate%', file_path],
                    universal_newlines=True,
                    shell=True,
                )
                video_bitrate = int(media_info_output_bitrate_video.strip())

                media_info_output_frame_rate = subprocess.check_output([
                    'MediaInfo.exe', '-f', '--Inform=Video;%FrameRate%', file_path],
                    universal_newlines=True,
                    shell=True,
                )
                video_frame_rate = float(media_info_output_frame_rate.strip())

                media_info_output_frame_count = subprocess.check_output([
                    'MediaInfo.exe', '-f', '--Inform=Video;%FrameCount%', file_path],
                    universal_newlines=True,
                    shell=True,
                )
                video_frame_count = int(media_info_output_frame_count.strip())

                media_info_output_duration_video = subprocess.check_output([
                    'MediaInfo.exe', '-f', '--Inform=Video;%Duration%', file_path],
                    universal_newlines=True,
                    shell=True,
                )
                video_duration = float(
                    media_info_output_duration_video.strip()) / 1000

                # Write media info to CSV
                writer.writerow([file_count, file_path, Path(file).name, media_duration, media_bitrate,
                                 video_format, video_resolution, video_bitrate, video_frame_rate,
                                 video_frame_count, video_duration])

logging.info(f"Total MP4 files processed: {file_count}")
logging.info(f"Media info written to {csv_file_path}")
