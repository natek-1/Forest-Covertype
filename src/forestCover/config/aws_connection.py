import os

import boto3
from dotenv import load_dotenv

load_dotenv()

class S3Client:

    def __init__(self, region=os.environ['AWS_REGION'], key_id=os.environ['AWS_ACCESS_KEY_ID'],
                 access_key =os.environ['AWS_SECRET_ACCESS_KEY']):
        self.s3_resource = boto3.resource("s3",
                                          aws_access_key_id=key_id,
                                          aws_secret_access_key=access_key,
                                          region_name=region
        )
        self.s3_client = boto3.client("s3",
                                        aws_access_key_id=key_id,
                                        aws_secret_access_key=access_key,
                                        region_name=region

        )

        
