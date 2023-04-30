import os
import sys
from google.cloud import storage


if len(sys.argv) != 4:
    print("Usage: python upload_csv.py project_id bucket_name directory_path")
    sys.exit(1)

project_id = sys.argv[1]
bucket_name = sys.argv[2]
directory_path = sys.argv[3]

directory_path = os.path.abspath(directory_path)

storage_client = storage.Client(project=project_id)

bucket = storage_client.bucket(bucket_name)

for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            blob = bucket.blob(file)
            blob.upload_from_filename(file_path)
