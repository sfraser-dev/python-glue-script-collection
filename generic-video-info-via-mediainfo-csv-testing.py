import subprocess

file_path = ".\sample-10s.mp4"  # Replace with the actual file path
# the_cur_dir = os.path.dirname(os.path.realpath(__file__))

media_info_output_duration = subprocess.check_output(
    ["MediaInfo.exe", "-f", "--Inform=General;%Duration%", file_path],
    universal_newlines=True,
    shell=True,
)
media_duration = float(media_info_output_duration.strip()) / 1000

print(media_info_output_duration)
print(media_duration)
