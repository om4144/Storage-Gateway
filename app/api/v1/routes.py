import io
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from app.services.object_store import ObjectStore
from app.db.models import ObjectRecord
from app.db.database import get_session

router = APIRouter()
storage = ObjectStore()


@router.put("/save")
async def put_object(file: UploadFile, session: Session = Depends(get_session)):
  # Task 1: upload the data and get back metadata
  try: 
    record = await storage.save(session= session, file=file)

  # Task 2: Raising error in case of failure
  except:
    raise HTTPException(
      status_code= 500,
      detail= "Failed to store data due to 'Internal Server Error'"
    )

  # Task 3: return record
  if record:
    return record

@router.get("/load")
async def get_object(object_id: str, session: Session = Depends(get_session)):
  # Task 1: Find key using object_id
  record = session.get(ObjectRecord, object_id)

  # Task 2: Raising exception if object id not found or invalid
  if not record:
    raise HTTPException(
      status_code= 404,
      detail= f"Bad Request: 'Invalid object id: {object_id}'"
    )

  # Task 3: upload the data and get back metadata
  try: 
    file = await storage.load(key=record.key)

  # Task 4: Raising error in case of failure
  except Exception as e:
    raise HTTPException(
      status_code= 500,
      detail= "Failed to load data due to 'Internal Server Error'"
    ) from e

  # Task 5: return file
  return StreamingResponse(
    file,
    media_type=record.content_type,
    headers={"Content-Disposition": f'attachment; filename="{record.filename}"'}
  )