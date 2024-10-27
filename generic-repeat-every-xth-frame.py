import os
import shutil
import logging

# Set up logging
logging.basicConfig(filename='zimg_processing.log', level=logging.INFO)

# Define the paths to the input and output directories
input_dir = '.'
output_dir = 'zimg'

# Set the repeat interval
repeat_every_xth_frame = 3

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Find all JPEG files in the input directory
input_files = [os.path.join(root, file) for root, _, files in os.walk(input_dir) for file in files if file.endswith('.jpg')]

# Process each JPEG file
file_count = 0
mod_count = 0

for input_file in input_files:
    # Get the filename without extension
    filename, extension = os.path.splitext(os.path.basename(input_file))

    # Create the output filename with leading zeros
    output_filename = f"zimg{file_count:09d}.jpg"

    # Copy the file to the output directory
    shutil.copy(input_file, os.path.join(output_dir, output_filename))

    # Log the file paths and copy status
    logging.info(f"{file_count}, {input_file}, {output_filename}")
    print(f"{file_count}, {input_file}, {output_filename}")

    # Check if it's time to repeat the previous file
    if mod_count == repeat_every_xth_frame:
        # Reset the "modulo" count
        mod_count = 0

        # Copy the previous file again
        file_count += 1
        output_filename = f"zimg{file_count:09d}.jpg"
        shutil.copy(input_file, os.path.join(output_dir, output_filename))

        # Log the repeated file copy
        logging.info(f"{file_count}, {input_file}, {output_filename} - repeated/copied")
        print(f"{file_count}, {input_file}, {output_filename} - repeated/copied")

    # Increment the file count and modulo count
    file_count += 1
    mod_count += 1
