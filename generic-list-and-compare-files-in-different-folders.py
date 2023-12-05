import os
import hashlib

# Uses dictionaries to store hash values with full-path-filenames
def compare_directories(path1, path2):
    # Create a dictionary to store unique elements for each directory
    directory1 = {}
    directory2 = {}

    # Find all files from the current and subdirectories
    for root, _, files in os.walk(path1):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hashlib.sha1(open(file_path, 'rb').read()).hexdigest()
            directory1[file_hash] = file_path

    for root, _, files in os.walk(path2):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hashlib.sha1(open(file_path, 'rb').read()).hexdigest()
            directory2[file_hash] = file_path

    # Find differences between the directories
    differences = []
    for file_hash in directory2:
        if file_hash not in directory1:
            differences.append(directory2[file_hash])

    return differences

if __name__ == '__main__':
    path1 = "C:\\Users\\toepo\\local\\git-weebucket\\python-glue-script-collection\\test1\\"
    path2 = "C:\\Users\\toepo\\local\\git-weebucket\\python-glue-script-collection\\test2\\"

    differences = compare_directories(path1, path2)
    for file in differences:
        print(file)
