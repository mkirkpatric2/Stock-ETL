import pandas as pd
import requests
from sqlalchemy import create_engine
from datetime import datetime
import argparse
from time import sleep

def change_dtypes(df):
    df.open = pd.to_numeric(df.open)
    df.high = pd.to_numeric(df.high)
    df.low = pd.to_numeric(df.low)
    df.close = pd.to_numeric(df.close)
    df.volume = pd.to_numeric(df.volume)
    df.date = pd.to_datetime(df.date)

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    rapidapi_key = params.rapidapi_key

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {"function": "TIME_SERIES_DAILY", "symbol": "MSFT", "outputsize": "full", "datatype": "json"}

    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data_unf = response.json()
    data_nar = data_unf['Time Series (Daily)']
    z = []
    for x, y in data_nar.items():
        y.update({'date': x})
        z.append(y)

    df = pd.DataFrame(z)
    df = df.rename(
        columns={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
    change_dtypes(df)
    df.to_sql(name=table_name, con=engine, if_exists='append')


    # now do periodic daily calls
    while True:
        sleep(86400)
        querystring = {"function": "TIME_SERIES_DAILY", "symbol": "MSFT", "outputsize": "compact", "datatype": "json"}
        response = requests.get(url, headers=headers, params=querystring)
        data_unf = response.json()
        data_nar = data_unf['Time Series (Daily)']
        z = []
        for x, y in data_nar.items():
            y.update({'date': x})
            z.append(y)
            break

        df = pd.DataFrame(z)
        df = df.rename(
            columns={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
        change_dtypes(df)
        df.to_sql(name=table_name, con=engine, if_exists='append')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('user', help='username for postgres')
    parser.add_argument('password', help='password for postgres')
    parser.add_argument('host', help='host for postgres')
    parser.add_argument('port', help='port for postgres')
    parser.add_argument('db', help='db name for postgres')
    parser.add_argument('table_name', help='table to add results to')
    parser.add_argument('rapidapi_key', help='table to add results to')

    args = parser.parse_args()

    main(args)