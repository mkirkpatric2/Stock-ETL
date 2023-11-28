FROM python:latest
WORKDIR /app
COPY . .
RUN pip install seaborn pandas boto3 s3fs fsspec

ENTRYPOINT ["python", "make_push_graphs.py"]

