from datetime import datetime
from sqlmodel import SQLModel, Field

class ObjectRecord(SQLModel, table=True):
  __tablename__ = "object_records"

  object_id: str = Field(
    primary_key=True, 
    description="Unique identifier for the object",
    schema_extra={"example": "obj_8f3a2b1c"},
  )

  key: str = Field(
    description="S3 object key/path",
    schema_extra={"example": "uploads/2026/09/report.pdf"}
  )

  filename: str = Field(
    description="Original filename of the uploaded object",
    schema_extra={"example": "quarterly_report.pdf"},
  )

  content_type: str = Field(
    description="MIME type of the object",
    schema_extra={"example": "application/pdf"}
  )

  created_at: datetime = Field(
    description="Timestamp when the record was created",
    schema_extra={"example": "2026-09-15T10:30:00Z"},
  )

  expire_at: datetime = Field(
    description="Timestamp when the object expires",
    schema_extra={"example": "2026-10-15T10:30:00Z"},
  )