import boto3
from app.core.config import get_settings

settings = get_settings()

class Client:
  def __init__(self):
    self.client = boto3.client(
      's3',
      endpoint_url=settings.CLOUD_ENDPOINT,
      aws_access_key_id=settings.ACCESS_TOKEN,
      aws_secret_access_key=settings.API_KEY,
      region_name=settings.REGION,
    )

client = Client().client