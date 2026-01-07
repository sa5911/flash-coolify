import os
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.storage import b2_storage

router = APIRouter()

# Define upload directory for local storage fallback
UPLOAD_DIR = Path(settings.UPLOADS_DIR) / "expenses"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file and return its URL. Uses B2 cloud storage if enabled, otherwise local storage."""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content
        content = await file.read()
        
        # Try B2 cloud storage first
        if b2_storage.is_enabled():
            success, url, error = await b2_storage.upload_file(
                file_content=content,
                filename=file.filename,
                content_type=file.content_type or "application/octet-stream",
                folder="expenses"
            )
            
            if success:
                return JSONResponse(
                    status_code=200,
                    content={
                        "success": True,
                        "url": url,
                        "path": url,
                        "filename": os.path.basename(url),
                        "original_filename": file.filename,
                        "storage": "b2"
                    }
                )
            else:
                # Log error but fall through to local storage
                print(f"[Upload] B2 upload failed: {error}, falling back to local storage")
        
        # Fallback to local storage
        file_ext = os.path.splitext(file.filename)[1]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        new_filename = f"{timestamp}_{unique_id}{file_ext}"
        
        file_path = UPLOAD_DIR / new_filename
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        file_url = f"/uploads/expenses/{new_filename}"
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "url": file_url,
                "path": file_url,
                "filename": new_filename,
                "original_filename": file.filename,
                "storage": "local"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@router.get("/storage/status")
async def storage_status():
    """Check the status of cloud storage configuration."""
    # Debug: Show raw settings values
    debug_info = {
        "B2_ENABLED_raw": settings.B2_ENABLED,
        "B2_KEY_ID_set": bool(settings.B2_KEY_ID),
        "B2_APPLICATION_KEY_set": bool(settings.B2_APPLICATION_KEY),
        "B2_BUCKET_NAME": settings.B2_BUCKET_NAME or "(not set)",
        "B2_ENDPOINT_URL": settings.B2_ENDPOINT_URL or "(not set)",
        "B2_REGION": settings.B2_REGION or "(not set)",
    }
    
    if b2_storage.is_enabled():
        success, message = b2_storage.test_connection()
        return {
            "b2_enabled": True,
            "b2_connected": success,
            "message": message,
            "bucket": settings.B2_BUCKET_NAME,
            "endpoint": settings.B2_ENDPOINT_URL,
            "debug": debug_info,
        }
    else:
        return {
            "b2_enabled": False,
            "b2_connected": False,
            "message": "B2 storage is not enabled. Using local storage.",
            "local_path": str(UPLOAD_DIR),
            "debug": debug_info,
        }


@router.post("/storage/test")
async def test_storage_upload():
    """Test upload functionality by uploading a small test file."""
    if not b2_storage.is_enabled():
        return {
            "success": False,
            "error": "B2 storage is not enabled. Set B2_ENABLED=true in environment variables.",
        }
    
    # Create a small test file
    test_content = b"This is a test file for B2 storage verification."
    
    success, url, error = await b2_storage.upload_file(
        file_content=test_content,
        filename="test.txt",
        content_type="text/plain",
        folder="test"
    )
    
    if success:
        return {
            "success": True,
            "message": "Test file uploaded successfully!",
            "url": url,
        }
    else:
        return {
            "success": False,
            "error": error,
        }
