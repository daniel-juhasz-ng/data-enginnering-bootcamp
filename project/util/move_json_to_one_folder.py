import os
import shutil

# Define the source and destination directories
src_dir = '/path/to/source/dir/'
dst_dir = '/path/to/destination/dir'

# Create the destination directory if it doesn't exist
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

# Recursively iterate through all files and directories in the source directory
for root, dirs, files in os.walk(src_dir):
    for file in files:
        # Check if the file is a JSON file
        if file.endswith('.json'):
            # Construct the full file path
            file_path = os.path.join(root, file)
            # Construct the new file path in the destination directory
            new_file_path = os.path.join(dst_dir, file)
            # Copy the file to the destination directory
            shutil.copy(file_path, new_file_path)
