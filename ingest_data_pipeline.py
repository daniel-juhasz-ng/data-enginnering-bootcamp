import pandas as pd
import pyarrow.parquet as pq
import argparse
from prefect_sqlalchemy import SqlAlchemyConnector
from prefect import task, flow
import requests
import io

chunk_size = 100000


@task
def extract(data_url: str):
    response = requests.get(data_url, stream=True)
    f = io.BytesIO(response.content)
    return pq.read_table(f).to_pandas()


@task
def transform(raw_data: pd.DataFrame):
    return raw_data.drop(raw_data[raw_data['passenger_count'].isna()].index)


@task
def load(data: pd.DataFrame, table_name: str, block_name: str):
    connector = SqlAlchemyConnector.load(block_name)

    with connector.get_connection(begin=False) as engine:
        # Create table
        data.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        chunks = list()
        num_chunks = len(data) // chunk_size + 1
        for i in range(num_chunks):
            chunks.append(data[i * chunk_size:(i + 1) * chunk_size])

        # Insert data
        for chunk in chunks:
            chunk.to_sql(name=table_name, con=engine, if_exists='append')
            print('Done with one')


@flow
def main_flow(args):
    extracted_data = extract(args.data_url)
    transformed_data = transform(extracted_data)
    load(transformed_data, args.table_name, args.sql_block_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NY Taxi data loader')
    parser.add_argument('--table_name', help='Table name for postgres')
    parser.add_argument('--data_url', help='URL for parquet data to load into postgres')
    parser.add_argument('--sql_block_name', help='Name of the Prefect SQL connection block')

    params = parser.parse_args()
    main_flow(params)

