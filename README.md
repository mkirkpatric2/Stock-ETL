<h1 style="text-align: center"> Stock-ETL</h1>

<h2 style="text-align: center">V2</h2>

V2 repurposes this app to run on AWS using: AWS Lambda, EventBridge, Elastic Container Service, Elastic Container Repository, and S3. All code is written in python. 

The webpage hosting the published graphs can be found: <a href="http://stock-data-buck1.s3-website.us-east-2.amazonaws.com/">HERE</a>

![Project Architecture Diagram](v2/stock-etl-v2.jpg "Project Architecture Diagram")

- Lambda
  - Performs ETL functions
    - Extracts data from the source API
    - Transforms the data for storage
    - Loads the data as a CSV into S3
  - Calls ECS to spin up the task that will process and publish graphs
- EventBridge
  - Triggers the lambda function to run daily
- Elastic Container Service (ECS)
  - Spins up the container containing the script which extracts the loaded data from S3 and creates graphs 
  - ECS runs daily as it is called each time the lambda function runs
- Elastic Container Repository (ECR)
  - Houses the image the ECS task uses when creating a container
- S3
  - Stores the processed data in CSV format
  - Stores the graphs published daily
  - Serves the graphs as part of a simple static webpage




<h2 style="text-align: center">V1</h2>
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
Python, ETL, Pandas, FastAPI, Relational Databases, Docker, AWS: Lambda, Eventbridge, ECS, ECR, S3, 
