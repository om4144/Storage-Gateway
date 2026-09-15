import pytest
from app.services.client import client

def test_client():
  res = client.list_buckets()

  buckets = [bucket["Name"] for bucket in res["Buckets"]]

  assert buckets[0] == "s3-storage"