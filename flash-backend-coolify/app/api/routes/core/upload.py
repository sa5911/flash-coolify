import os
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.core.file import File as FileModel
from app.schemas.core.file import FileResponse
from app.api.dependencies import get_current_user
from app.models.core.user import User

router = APIRouter()

# Default upload directory for status check
UPLOAD_DIR = Path(settings.UPLOADS_DIR) / "uploads"


@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Query("uploads", description="Folder to upload to"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a file and return its URL.
    Stores file locally and saves metadata to the database.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content
        content = await file.read()
        
        # Determine MIME type if missing
        mime_type = file.content_type or "application/octet-stream"
        
        original_filename = file.filename
        
        # Local storage logic
        file_ext = os.path.splitext(original_filename)[1]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        new_filename = f"{timestamp}_{unique_id}{file_ext}"

        local_upload_dir = Path(settings.UPLOADS_DIR) / folder
        local_upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = local_upload_dir / new_filename
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        unique_filename_db = new_filename
        public_path = f"/uploads/{folder}/{new_filename}" 
        storage_type = "local"
        
        # Save to database
        db_file = FileModel(
            filename=original_filename,
            unique_filename=unique_filename_db,
            path=public_path,
            storage_type=storage_type,
            mime_type=mime_type,
            size=len(content),
            user_id=current_user.id
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_file
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@router.get("/storage/status")
async def storage_status():
    """Check the status of storage configuration."""
    return {
        "storage_type": "local",
        "local_path": str(UPLOAD_DIR),
        "message": "Using local storage.",
    }
