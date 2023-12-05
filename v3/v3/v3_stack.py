from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
)
from constructs import Construct

class V3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "AAPL_buck",
                           website_index_document="index.html",
                           public_read_access=True, versioned=False)

        extract_lambda = _lambda.Function(self, 'create_lambda',
                                          runtime=_lambda.Runtime.PYTHON_3_11,
                                          handler="extractor.lambda_handler",
                                          code=_lambda.Code.from_asset("./extractor"),
                                          environment=dict(
                                              -fill-
                                          ))

        #ECS - figure out how to use boto3 to send info into the script running on ECS