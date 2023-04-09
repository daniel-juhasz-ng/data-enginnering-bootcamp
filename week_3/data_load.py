import requests
import sys
from google.cloud import storage
<<<<<<< HEAD
=======
import io
>>>>>>> a25f891fc9741453b7577e1faa843d36a1557c69

file_url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/'

client = storage.Client()
bucket = client.bucket(sys.argv[3])
base_name = '{service}_tripdata_{request_year}-{request_month:02d}.csv.gz'

<<<<<<< HEAD
for i in range(0, 1):
    file_name = base_name.format(service=sys.argv[1],request_year=sys.argv[2], request_month=i + 1)

    response = requests.get(file_url_prefix + file_name)
    print('File downloaded - {}'.format(file_name))
    blob = bucket.blob(file_name)

    blob.upload_from_string(response.text, timeout=180)
    print('File uploaded - {}'.format(file_name))
=======
for i in range(12):
    file_name = base_name.format(service=sys.argv[1], request_year=sys.argv[2], request_month=i + 1)

    response = requests.get(file_url_prefix + file_name, stream=True)
    print('File downloaded - {}'.format(file_name))
    blob = bucket.blob(file_name)

    blob.upload_from_file(io.BytesIO(response.content), timeout=180, content_type='application/gzip')
    print('File uploaded - {}'.format(file_name))
>>>>>>> a25f891fc9741453b7577e1faa843d36a1557c69
