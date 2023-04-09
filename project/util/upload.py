import os
from google.cloud import storage

# Replace with your project ID and bucket name
project_id = 'your-project-id'
bucket_name = 'your-bucket-name'

# Create a client object to access the Google Storage API
storage_client = storage.Client(project=project_id)

# Get the bucket object to upload the files
bucket = storage_client.bucket(bucket_name)

# Recursively iterate through all files and directories from the current directory
for root, dirs, files in os.walk('..'):
    for file in files:
        # Check if the file is a JSON file
        if file.endswith('.json'):
            # Construct the full file path
            file_path = os.path.join(root, file)
            # Create a blob object for the file
            blob = bucket.blob(file_path)
            # Upload the file to the bucket
            blob.upload_from_filename(file_path)
