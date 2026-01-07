"""
File upload helper module.

Provides a unified upload function that enforces local storage.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Tuple

from app.core.config import settings


async def upload_file_to_storage(
    content: bytes,
    original_filename: str,
    content_type: str = "application/octet-stream",
    folder: str = "uploads",
    local_subdir: str = "uploads",
) -> Tuple[str, str]:
    """
    Upload a file to local storage.
    
    Args:
        content: File content as bytes
        original_filename: Original filename (for extension)
        content_type: MIME type
        folder: Not used (kept for compatibility)
        local_subdir: Subdirectory under UPLOADS_DIR for local storage
    
    Returns:
        Tuple of (url, storage_type) where storage_type is always "local"
    """
    # Generate unique filename
    ext = os.path.splitext(original_filename)[1] if original_filename else ""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    new_filename = f"{timestamp}_{unique_id}{ext}"
    
    # Local storage
    local_dir = Path(settings.UPLOADS_DIR) / local_subdir
    local_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = local_dir / new_filename
    with open(file_path, "wb") as f:
        f.write(content)
    
    local_url = f"/uploads/{local_subdir}/{new_filename}"
    return local_url, "local"


async def upload_file_with_prefix(
    content: bytes,
    original_filename: str,
    prefix: str,
    content_type: str = "application/octet-stream",
    folder: str = "uploads",
    local_subdir: str = "uploads",
) -> Tuple[str, str, str]:
    """
    Upload a file with a custom prefix to local storage.
    
    Args:
        content: File content as bytes
        original_filename: Original filename (for extension)
        prefix: Prefix for the filename (e.g., "emp123_avatar")
        content_type: MIME type
        folder: Not used (kept for compatibility)
        local_subdir: Subdirectory under UPLOADS_DIR for local storage
    
    Returns:
        Tuple of (url, new_filename, storage_type)
    """
    # Generate unique filename with prefix
    ext = os.path.splitext(original_filename)[1] if original_filename else ""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    new_filename = f"{prefix}_{timestamp}_{unique_id}{ext}"
    
    # Local storage
    local_dir = Path(settings.UPLOADS_DIR) / local_subdir
    local_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = local_dir / new_filename
    with open(file_path, "wb") as f:
        f.write(content)
    
    local_url = f"/uploads/{local_subdir}/{new_filename}"
    return local_url, new_filename, "local"
