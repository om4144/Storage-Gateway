import io
import asyncio
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi import UploadFile
from botocore.exceptions import ClientError
from sqlmodel import Session

from app.db.models import ObjectRecord
from app.services.client import client
from app.core.config import get_settings

settings = get_settings()

class ObjectStore:
  def __init__(self):
    self.client = client
    self.bucket = settings.BUCKET

  async def save(
    self,
    session: Session,
    file: UploadFile,
    ttl_days: int = settings.TTL
  ) -> dict:

    # Task 1: generate object_id and key
    object_id: str = str(uuid4())
    key: str = f"objects/{object_id}/{file.filename}"

    # Task 2: upload the object to bucket
    await asyncio.to_thread(
      self.client.upload_fileobj, 
      file.file, 
      self.bucket, 
      key
    )

    # Task 3: calculate created_at and expire_at dates
    now = datetime.now(timezone.utc)
    expire_at = now + timedelta(days= ttl_days)

    # Task 4: Save metadata in database
    record = ObjectRecord(
      object_id= object_id,
      key= key,
      filename= file.filename,
      content_type= file.content_type,
      created_at= now, 
      expire_at= expire_at,
    )

    session.add(record)
    session.commit()

    # Task 5: return the data
    return {
      "object_id": object_id,
      "key": key,
      "filename": file.filename,
      "content_type": file.content_type,
      "created_at": now.isoformat(),
      "expires_at": expire_at.isoformat(),
    }

  async def load(self, key: str) -> io.BytesIO:
    # Task 1: create a In memory buffer using BytesIO
    buffer = io.BytesIO()

    # Task 2: load the data from cloud
    await asyncio.to_thread(
      self.client.download_fileobj, 
      self.bucket, 
      key, 
      buffer
    )

    # Task 3: Wrtite data into buffer
    buffer.seek(0)

    # Task 4: return the buffer file
    return buffer

  async def delete(
    self,
    session: Session,
    object_id: str,
    key: str,
  ) -> None:
    # Task 1: try to delete object
    try:
      await asyncio.to_thread(
        self.client.delete_object,
        Bucket= self.bucket,
        Key= key,
      )

    # Task 2: Raise an error if deletion failed
    except ClientError as e:
      raise RuntimeError(f"ailed to delete object '{key}' from storage: {e}")

    # Task 3: Find the object using object_id
    record = session.get(ObjectRecord, object_id)
    if record:
      # task 4: on successfull retrival delete the meta data from the ObjectStore
      session.delete(record)
      session.commit()

  async def metadata(
    self,
    session: Session,
    object_id: str
  ) -> dict | None:
    # Task 1: get the data using object_id
    record = session.get(ObjectRecord, object_id)

    # Task 2: if not found return none
    if not record:
      return None

    # Task 3: if found return the data

    return {
      "object_id": record.object_id,
      "filename": record.filename,
      "content_type": record.content_type,
      "created_at": record.created_at.isoformat(),
      "expires_at": record.expires_at.isoformat(),
    }
