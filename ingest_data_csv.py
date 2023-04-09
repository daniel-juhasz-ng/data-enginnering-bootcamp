from sqlalchemy import create_engine
import argparse
import pandas as pd
from time import time


def main(params):
    db_name = params.db_name
    user = params.user
    host = params.host
    port = params.port
    table_name = params.table_name
    password = params.password

    chunk_size = 100000
    filename = 'taxi_zone_lookup.csv'

    header = pd.read_csv(filename, nrows=1)

    df_iter = pd.read_csv(filename, iterator=True, chunksize=chunk_size)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    engine.connect()

    header.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            df.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()
            print('inserted another chunk, took %.3f second' % (t_end - t_start))
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break


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
