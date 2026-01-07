"""
Backblaze B2 Cloud Storage Service

This module provides S3-compatible cloud storage integration with Backblaze B2.
It can be used as a drop-in replacement for local file storage.
"""

import os
import uuid
from datetime import datetime
from typing import Optional, Tuple
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from app.core.config import settings


class B2StorageService:
    """Backblaze B2 storage service using S3-compatible API."""
    
    _client = None
    
    @classmethod
    def get_client(cls):
        """Get or create S3 client for B2."""
        if cls._client is None and settings.B2_ENABLED:
            cls._client = boto3.client(
                "s3",
                endpoint_url=settings.B2_ENDPOINT_URL,
                aws_access_key_id=settings.B2_KEY_ID,
                aws_secret_access_key=settings.B2_APPLICATION_KEY,
                region_name=settings.B2_REGION,
            )
        return cls._client
    
    @classmethod
    def is_enabled(cls) -> bool:
        """Check if B2 storage is enabled and configured."""
        return (
            settings.B2_ENABLED
            and settings.B2_KEY_ID
            and settings.B2_APPLICATION_KEY
            and settings.B2_BUCKET_NAME
            and settings.B2_ENDPOINT_URL
        )
    
    @classmethod
    def generate_filename(cls, original_filename: str, prefix: str = "") -> str:
        """Generate a unique filename with timestamp and UUID."""
        ext = os.path.splitext(original_filename)[1] if original_filename else ""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        
        if prefix:
            return f"{prefix}/{timestamp}_{unique_id}{ext}"
        return f"{timestamp}_{unique_id}{ext}"
    
    @classmethod
    async def upload_file(
        cls,
        file_content: bytes,
        filename: str,
        content_type: str = "application/octet-stream",
        folder: str = "uploads"
    ) -> Tuple[bool, str, str]:
        """
        Upload a file to B2 cloud storage.
        
        Args:
            file_content: The file content as bytes
            filename: Original filename (used to extract extension)
            content_type: MIME type of the file
            folder: Folder/prefix in B2 bucket
        
        Returns:
            Tuple of (success, url, error_message)
        """
        if not cls.is_enabled():
            return False, "", "B2 storage is not enabled"
        
        try:
            client = cls.get_client()
            
            # Generate unique key
            key = cls.generate_filename(filename, prefix=folder)
            
            # Upload to B2
            client.put_object(
                Bucket=settings.B2_BUCKET_NAME,
                Key=key,
                Body=file_content,
                ContentType=content_type,
            )
            
            # Generate public URL
            # Backblaze B2 friendly URL format
            public_url = f"https://f005.backblazeb2.com/file/{settings.B2_BUCKET_NAME}/{key}"
            
            return True, public_url, ""
            
        except ClientError as e:
            error_msg = str(e)
            print(f"[B2] Upload error: {error_msg}")
            return False, "", error_msg
        except Exception as e:
            error_msg = str(e)
            print(f"[B2] Unexpected error: {error_msg}")
            return False, "", error_msg
    
    @classmethod
    async def delete_file(cls, key: str) -> Tuple[bool, str]:
        """
        Delete a file from B2 cloud storage.
        
        Args:
            key: The object key/path in B2
        
        Returns:
            Tuple of (success, error_message)
        """
        if not cls.is_enabled():
            return False, "B2 storage is not enabled"
        
        try:
            client = cls.get_client()
            client.delete_object(
                Bucket=settings.B2_BUCKET_NAME,
                Key=key,
            )
            return True, ""
        except ClientError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
    
    @classmethod
    def test_connection(cls) -> Tuple[bool, str]:
        """
        Test the B2 connection.
        
        Returns:
            Tuple of (success, message)
        """
        if not cls.is_enabled():
            return False, "B2 storage is not enabled or not fully configured"
        
        try:
            client = cls.get_client()
            # Try to list objects (with max 1) to verify connection
            response = client.list_objects_v2(
                Bucket=settings.B2_BUCKET_NAME,
                MaxKeys=1
            )
            return True, f"Connected to bucket: {settings.B2_BUCKET_NAME}"
        except ClientError as e:
            return False, f"Connection failed: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"


# Singleton instance
b2_storage = B2StorageService()
