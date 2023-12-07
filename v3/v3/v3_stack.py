from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_iam as iam,
)
from constructs import Construct


class V3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "AAPL_buck")

        layer_pandassdk = _lambda.LayerVersion.from_layer_version_arn(self, 'pandas_layer',
                                                                      'arn:aws:lambda:us-east-2:336392948345:layer:AWSSDKPandas-Python311:4')

        layer_requests = _lambda.LayerVersion.from_layer_version_arn(self, 'requests_layer',
                                                                     'arn:aws:lambda:us-east-2:737038835517:layer:requests:1')

        extract_lambda = _lambda.Function(self, 'create_lambda',
                                          runtime=_lambda.Runtime.PYTHON_3_11,
                                          code=_lambda.Code.from_asset("./lambda"),
                                          handler="extractor.handler",
                                          environment=dict({
                                              'BUCK_NAME': bucket.bucket_name,
                                              'API_KEY': '',
                                              # fill in w/ your RapidAPIkey for Alpha-Vantage
                                              'STOCK': "AAPL"  # fill in as desired
                                          }),
                                          layers=[layer_pandassdk, layer_requests],
                                          timeout=Duration.seconds(15))

        s3_listbuckets_policy = iam.PolicyStatement(actions=['s3:ListAllMyBuckets'],
                                                    resources=['arn:aws:s3:::*'])
        extract_lambda.add_to_role_policy(s3_listbuckets_policy)

        bucket.grant_write(extract_lambda)

        events.Rule(self, 'daily-lambda-rule',
                    description='Trigger lambda daily',
                    targets=[events_targets.LambdaFunction(extract_lambda)],
                    schedule=events.Schedule.rate(Duration.hours(24)))

        # ECS - Rebuild the image to be modular. Remove hardcoded references to bucket + stock name
        # use boto3 ecs.runtask to provide overrides which assign new environ variables based
        # on what is passed in via lambda. Assign these variables as environ variables for lambda here.
