import os
import subprocess
from pathlib import Path

# use forward slashes ('/') in the pathname
vid_originals_folder = "C:/Users/toepo/local/git-weebucket/python-glue-script-collection"  

if os.path.isdir(vid_originals_folder):
    print(f"Converting videos in folder '{vid_originals_folder}' and its sub-folders")
else:
    print(f"Error: Folder '{vid_originals_folder}' doesn't exist. Please point to the folder containing the videos to be converted.")
    exit()

content = []
all_arr = []

#  find the video files from the specified directory and its sub-directories
for root, dirs, files in os.walk(vid_originals_folder):
    for file in files:
        if file.lower().endswith(".mp4"):
            content.append(os.path.join(root, file))

for vid_name in content:
    # get filename, directory, and extension of the found video
    name, file_dir, ext = Path(vid_name).stem, Path(vid_name).parent, Path(vid_name).suffix
    # convert forward slashes to backward slashes
    file_dir = file_dir.as_posix().replace("/", "\\") 
    # will add trailing slash if not already there
    found_complete_name = os.path.join(file_dir,name+ext)    
    new_complete_name = os.path.join(file_dir, name+"-new"+ext)
    str_data = f"{found_complete_name}==={new_complete_name}"
    # full paths of videos to be converted stored in a list
    all_arr.append(str_data)

# read pathnames from the list and run FFmpeg to convert
for item in all_arr:
    splitter = item.split("===")
    original_file_name_full_path, converted_file_name_full_path = splitter[0], splitter[1]
    # print(original_file_name_full_path)
    # print(converted_file_name_full_path)
    subprocess.run(["ffmpeg", "-i", original_file_name_full_path, "-f", "mp4", "-crf", "38", converted_file_name_full_path])