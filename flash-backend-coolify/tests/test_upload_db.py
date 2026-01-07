import sys
import os
import io
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.core.config import settings
from app.api.dependencies import get_current_user
from app.models.core.user import User
from app.models.core.file import File
from app.core.database import get_db

# Mock user
def override_get_current_user():
    return User(id=1, username="testuser", is_active=True, is_superuser=True)

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_upload_and_db_persistence():
    print("Testing upload and DB persistence...")
    
    # Create test file content
    file_content = b"Content for DB verification test"
    file_name = "db_test_file.txt"
    
    # Upload
    response = client.post(
        "/api/upload",
        files={"file": (file_name, file_content, "text/plain")},
        params={"folder": "test_verification"}
    )
    
    if response.status_code != 200:
        print(f"FAILED: Upload failed with status {response.status_code}")
        print(response.json())
        sys.exit(1)
        
    data = response.json()
    print("Upload response:", data)
    
    file_id = data.get("id")
    if not file_id:
        print("FAILED: No file ID returned in response")
        sys.exit(1)
        
    # Verify in DB
    print(f"Verifying file ID {file_id} in database...")
    
    # Connect to DB directly
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        db_file = db.query(File).filter(File.id == file_id).first()
        if not db_file:
            print("FAILED: File record not found in database")
            sys.exit(1)
            
        print(f"SUCCESS: Found file in DB!")
        print(f"  - ID: {db_file.id}")
        print(f"  - Filename: {db_file.filename}")
        print(f"  - Unique Filename: {db_file.unique_filename}")
        print(f"  - Path: {db_file.path}")
        print(f"  - Storage Type: {db_file.storage_type}")
        print(f"  - Size: {db_file.size}")
        
        # Verify file exists on disk (if local)
        if db_file.storage_type == "local":
            full_path = os.path.join(settings.UPLOADS_DIR, "test_verification", db_file.unique_filename)
            if os.path.exists(full_path):
                print(f"SUCCESS: File found on disk at {full_path}")
            else:
                print(f"FAILED: File not found on disk at {full_path}")
                sys.exit(1)
                
    finally:
        db.close()

if __name__ == "__main__":
    test_upload_and_db_persistence()
