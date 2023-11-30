import os
import pathlib
import logging
from arraydiff import arraydiff

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('script.log')
logger.addHandler(handler)

# Define the paths to the two directories
path1 = "F:\\dev7_2016_10p4\\GitRepo_J\\vss2016_10p4_vstudio2015\\bin\\release\\DorsaLista\\"
path2 = "C:\\VitecC9SDK\\VM4C9_1_05_03\\extractHere\\DL_vm4c9sdk_v01.05.03Copy\\bin\\DorsaLista"

# Collect file names from the first directory
files1 = []
for root, _, files in os.walk(path1):
    for file in files:
        files1.append(file)

# Collect file names from the second directory
files2 = []
for root, _, files in os.walk(path2):
    for file in files:
        files2.append(file)

# Find the differences between the two sets of files
differences = arraydiff(files1, files2)

# Log the file names
logger.info("-------------------------------")
logger.info("File names in folder 1:")
for file in files1:
    logger.info(file)

logger.info("-------------------------------")
logger.info("File names in folder 2:")
for file in files2:
    logger.info(file)

logger.info("-------------------------------")
logger.info("Differences:")
for file in differences:
    logger.info(file)

