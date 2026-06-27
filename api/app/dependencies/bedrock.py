import os
import boto3
from functools import lru_cache
import logging
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_bedrock_client():
    try:
        return boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
    except (BotoCoreError, ClientError) as e:
        logging.exception(f"Failed to initialize AWS Bedrock client: {str(e)}")
        # We MUST re-raise so @lru_cache knows NOT to cache this failure
        raise e