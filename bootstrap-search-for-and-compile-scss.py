import os
import subprocess
import pathlib

# Specify the target directory for Sass files
target_dir = "."

# Create a list to store the paths of Sass files
sass_files = []

# Find all Sass files in the target directory
for root, _, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".scss"):
            sass_files.append(os.path.join(root, file))

# Create a directory for CSS files if it doesn't exist
css_dir = pathlib.Path("../css")
css_dir.mkdir(parents=True, exist_ok=True)

# Compile each Sass file to CSS (normal and minified)
for sass_file in sass_files:
    # Get the file name, directory, and extension
    filename, file_dir, ext = os.path.splitext(os.path.basename(sass_file))

    # Ignore Sass partials (filenames begin with underscore)
    if filename.startswith("_"):
        continue

    # Define input and output file names
    input_file = os.path.join(file_dir, filename + ext)
    output_file = os.path.join(css_dir, filename + ".css")
    minified_output_file = os.path.join(css_dir, filename + ".min.css")

    # Compile Sass file to normal CSS
    subprocess.run(["sass", input_file, output_file, "--no-source-map"])

    # Compile Sass file to minified CSS
    subprocess.run(["sass", input_file, minified_output_file, "--no-source-map", "--style", "compressed"])

