import pyarrow.parquet as pq
from sqlalchemy import create_engine
import argparse
import os
import pandas as pd


def main(params):
    db_name = params.db_name
    user = params.user
    host = params.host
    port = params.port
    table_name = params.table_name
    data_url = params.data_url
    password = params.password

    chunk_size = 100000
    filename = 'out.parquet'

    os.system(f'curl {data_url} -o {filename}')

    pd.read_csv('filename and path', nrows=100)



    trips = pq.read_table(filename)
    trips = trips.to_pandas()

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    engine.connect()

    trips.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    chunks = list()
    num_chunks = len(trips) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(trips[i * chunk_size:(i + 1) * chunk_size])

    for chunk in chunks:
        chunk.to_sql(name=table_name, con=engine, if_exists='append')
        print('Done with one')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NY Taxi data loader')
    parser.add_argument('db_name', help='Database name for postgres')
    parser.add_argument('password', help='Password for postgres')
    parser.add_argument('user', help='User name for postgres')
    parser.add_argument('host', help='Host name for postgres')
    parser.add_argument('port', help='Port for postgres')
    parser.add_argument('table_name', help='Table name for postgres')
    parser.add_argument('data_url', help='URL for parquet data to load into postgres')

    args = parser.parse_args()

    main(args)
