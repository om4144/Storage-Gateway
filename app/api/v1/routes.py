from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlmodel import Session

from app.services.object_store import ObjectStore
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