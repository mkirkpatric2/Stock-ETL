FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install fastapi psycopg2 pydantic SQLalchemy starlette uvicorn python-decouple
EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]