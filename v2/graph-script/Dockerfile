FROM python:latest
WORKDIR /app
RUN pip install seaborn pandas boto3

ENTRYPOINT ["python", "/app/make_push_graphs.py"]