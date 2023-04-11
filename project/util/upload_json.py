import os
import sys
from google.cloud import storage

# Check if the correct number of arguments are provided
if len(sys.argv) != 4:
    print("Usage: python script.py project_id bucket_name directory_path")
    sys.exit(1)

# Get the project_id, bucket_name, and directory_path from command line arguments
project_id = sys.argv[1]
bucket_name = sys.argv[2]
directory_path = sys.argv[3]

# Convert the directory_path to an absolute path
directory_path = os.path.abspath(directory_path)

# Create a client object to access the Google Storage API
storage_client = storage.Client(project=project_id)

# Get the bucket object to upload the files
bucket = storage_client.bucket(bucket_name)

# Recursively iterate through all files and directories in the given directory path
for root, dirs, files in os.walk(directory_path):
    for file in files:
        # Check if the file is a JSON file
        if file.endswith('.json'):
            # Construct the full file path
            file_path = os.path.join(root, file)
            # Create a blob object for the file
            blob = bucket.blob(file_path)
            # Upload the file to the bucket
            blob.upload_from_filename(file_path)
