from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class FileBase(BaseModel):
    filename: str
    content_type: Optional[str] = None

class FileCreate(FileBase):
    pass

class FileResponse(FileBase):
    id: int
    unique_filename: str
    path: str
    storage_type: str
    mime_type: str
    size: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
