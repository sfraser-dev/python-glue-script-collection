import os
import pathlib
import re

# Create a list to store the XML files
xml_files = []

# Find all XML files in the current directory and its subdirectories
for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.xml'):
            xml_files.append(os.path.join(root, file))

# Process each XML file
for xml_file in xml_files:
    # Read the contents of the XML file
    with open(xml_file, 'r') as f:
        xml_content = f.read()

    # Replace the specified text
    processed_content = re.sub(r"oldy", r"newStuff", xml_content)

    # Write the processed content to a new file
    new_file_path = xml_file + '.new'
    with open(new_file_path, 'w') as f:
        f.write(processed_content)

    # Optionally, write the processed content back to the original file
    # with open(xml_file, 'w') as f:
    #     f.write(processed_content)

