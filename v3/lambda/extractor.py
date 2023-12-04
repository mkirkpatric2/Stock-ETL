import boto3
from pandas import DataFrame
import requests
import os

# Use AWSSDK Pandas layer
# Uploaded personal 'requests' layer


def lambda_handler(event, context):
    client = boto3.client('s3')
    client_ecs = boto3.client('ecs')

    bucket_name = ''
    api_key = ''
    cluster = ''
    taskDefinition = os.environ['taskDefinition']
    sn1 = os.environ['sn1']
    sn2 = os.environ['sn2']
    sn3 = os.environ['sn3']
    sec_group = os.environ['sec_group']

    bucket_list = []
    response = client.list_buckets()

    for bucket in response["Buckets"]:
        bucket_list.append(bucket['Name'])

    if bucket_name not in bucket_list:
        client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'us-east-2'
            },
        )

    url = "https://alpha-vantage.p.rapidapi.com/query"
    querystring = {"function": "TIME_SERIES_DAILY", "symbol": "MSFT", "outputsize": "full", "datatype": "json"}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data_unf = response.json()
    del response

    data_nar = data_unf['Time Series (Daily)']
    z = []
    for x, y in data_nar.items():
        y.update({'date': x})
        z.append(y)

    del data_unf
    del data_nar

    df = DataFrame(z)
    del z
    df = df.rename(
        columns={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})

    df.to_csv('/tmp/msft-daily-data.csv', index=False)

    client.upload_file("/tmp/msft-daily-data.csv", bucket_name, "msft-daily-data.csv")

    response = client_ecs.run_task(
        cluster=cluster,
        count=1,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    sn1,
                    sn2,
                    sn3
                ],
                'securityGroups': [
                    sec_group,
                ],
                'assignPublicIp': 'ENABLED'
            }
        },
        taskDefinition=taskDefinition,
    )

    return "csv created"
