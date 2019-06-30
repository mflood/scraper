

import os
import boto3

DEFAULT_REGION_NAME = 'us-east-1'

def build_sqs_client():
    """
        Returns an SQS client
    """

    api_key=os.getenv('AWS_KEY_ID')
    api_secret=os.getenv('AWS_SECRET')
    sqs_client = boto3.client('sqs',
                              region_name=DEFAULT_REGION_NAME,
                              aws_access_key_id=api_key,
                              aws_secret_access_key=api_secret)

    return sqs_client

#end
