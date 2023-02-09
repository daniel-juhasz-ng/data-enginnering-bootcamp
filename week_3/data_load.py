import requests
import sys
from google.cloud import storage
import io

file_url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/'

client = storage.Client()
bucket = client.bucket(sys.argv[3])
base_name = '{service}_tripdata_{request_year}-{request_month:02d}.csv.gz'

for i in range(12):
    file_name = base_name.format(service=sys.argv[1], request_year=sys.argv[2], request_month=i + 1)

    response = requests.get(file_url_prefix + file_name, stream=True)
    print('File downloaded - {}'.format(file_name))
    blob = bucket.blob(file_name)

    blob.upload_from_file(io.BytesIO(response.content), timeout=180, content_type='application/gzip')
    print('File uploaded - {}'.format(file_name))