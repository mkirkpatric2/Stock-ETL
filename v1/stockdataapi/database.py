from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import environ as env
import psycopg2
from decouple import config

db_user = config('db_user')
db_password = config('db_password')
db_host = config('db_host')
db_port = config('db_port')
db_name = config('db_name')

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# check_same_thread: False mandates only one thread active at a time
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#bind to engine above. ensure autocommit/autoflush are false
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()