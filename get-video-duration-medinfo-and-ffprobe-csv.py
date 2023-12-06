import os
import subprocess
from pathlib import Path

content = []
file_count = 0

# create a log file using pathlib Path
perl_filename_base = Path(__file__).stem
log_file = f"{perl_filename_base}.log"
with open(log_file, 'w') as fh:
    fh.write("fileCount, vidDurMI, vidDurFF, filePath, fileName\n")

# get the directory (full path) of this script using os.path
the_cur_dir = os.path.dirname(os.path.realpath(__file__))
print(f"the_cur_dir = {the_cur_dir}")

if os.path.isdir(the_cur_dir):
    print(f"Analysing videos in folder '{the_cur_dir}' and its sub-folders")
else:
    print(f"Error: Folder '{the_cur_dir}' doesn't exist.") 
    exit()

# look for files in this folder and sub-folders, store them in a list
for root, dirs, files in os.walk(the_cur_dir):
    for file in files:
        if file.lower().endswith(".mp4"):
            file_count += 1
            content.append(os.path.join(root, file))

with open (log_file, 'a') as fh:
    # loop over list of found files
    for vid_name in content:
        # get filename, directory, and extension of the found file
        name, file_dir, ext = Path(vid_name).stem, Path(vid_name).parent, Path(vid_name).suffix
        # convert forward slashes to backward slashes
        file_dir = file_dir.as_posix().replace("/", "\\") 
        # full pathname of found file constructed by OS agnostic os.path
        found_complete_name = os.path.join(file_dir,name+ext)    

        # mediainfo
        vid_dur_mi = int(subprocess.check_output(["MediaInfo.exe", "-f", "--Inform=Video;%Duration%", found_complete_name]).decode('utf-8')) / 1000
        print(f"vid_dur_mi = {vid_dur_mi}")

        # ffprobe
        probe_info = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", found_complete_name]).decode('utf-8').split('\n')
        vid_dur_ff = next(line.split('=')[1] for line in probe_info if "duration" in line)
        vid_dur_ff = vid_dur_ff.strip()
        vid_dur_ff = float(vid_dur_ff) if "." in vid_dur_ff else int(vid_dur_ff)
        print(f"vid_dur_ff = {vid_dur_ff}")

        # log results
        fh.write(f"{file_count}, {vid_dur_mi}, {vid_dur_ff}, {file_dir}, {name+ext}\n")

fh.close()