# Stock-ETL
Dockerized ETL script packaged w/ rudimentary API for access to data. 

When running the ETL script, provide the following as arguments in this order:
1. 'user', help='username for postgres'
2. 'password', help='password for postgres'
3. 'host', help='host for postgres'
4. 'port', help='port for postgres'
5. 'db', help='db name for postgres'
6. 'table_name', help='table to add results to'
7. 'rapidapi_key', help='table to add results to'

When running the API, create a .env file in the API's root folder w/ the following structure:\
db_user=''\
db_password=''\
db_host=''\
db_port=\
db_name=''

If running locally as dockerized microservices (including your DB), ensure that each container is part of the same Docker Network. 


# Skills Highlighted
Python, ETL, Pandas, FastAPI, Relational Databases, Docker
