
# (Work in progress) V3 - Stock ETL

This version of the project will provide a modular version of what V2 provides using AWS CDK (and CloudFormation) to build and deploy the infrastructure. 

Currently, the app only build and deploys the S3 bucket and the Lambda function. With respect to these functions, the project is operational. This part is modular  as a user can change the defined stock in the cdk stack to eventually deploy a version centered around the given stock. 

## Remaining additions to be made:

ECR: A new image will be added that does not have the bucket nor the stock hardcoded. The modified image will enable (1) the same image to be used with multiple deployments, and (2) a user to change the desired stock in the CDK files and have the changes reflected downstream.

ECS: A taskdefinition will be written in the stack using the new image. 

Lambda: a boto3.runtask function will be called as in V2. This time, the function will provide the image additional environment variables reflecting the stock given by the user and the bucket name created by CloudFormation upon deployment. 
