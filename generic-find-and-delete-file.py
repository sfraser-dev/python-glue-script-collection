import os
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('script.log')
logger.addHandler(handler)

file_count = 0

# Find all files with .scc or .vspscc extension in the current directory and its subdirectories
for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.bst') or file.endswith('.hx'):
            file_count += 1
            file_path = os.path.join(root, file)
            logger.info(f"{file_count}, {file_path}")

            # Delete the file
            try:
                os.remove(file_path)
            except OSError as e:
                logger.error(f"Failed to delete file: {file_path}")
                logger.exception(e)

logging.info(f"Total files deleted: {file_count}")

