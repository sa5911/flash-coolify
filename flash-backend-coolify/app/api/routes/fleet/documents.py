import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.upload_helper import upload_file_with_prefix
from app.models.fleet.vehicle import Vehicle
from app.models.fleet.vehicle_document import VehicleDocument
from app.schemas.fleet.vehicle_document import VehicleDocumentOut


router = APIRouter()


def _upload_dir() -> str:
    d = os.path.join(os.path.abspath(settings.UPLOADS_DIR), "vehicles")
    os.makedirs(d, exist_ok=True)
    return d


def _public_url(path: str) -> str:
    fn = os.path.basename(path)
    return f"/uploads/vehicles/{fn}"


@router.get("/{vehicle_id}/documents", response_model=List[VehicleDocumentOut])
async def list_vehicle_documents(vehicle_id: str, db: Session = Depends(get_db)) -> List[VehicleDocumentOut]:
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    docs = (
        db.query(VehicleDocument)
        .filter(VehicleDocument.vehicle_id == vehicle_id)
        .order_by(VehicleDocument.id.desc())
        .all()
    )

    out: List[VehicleDocumentOut] = []
    for d in docs:
        url = d.path if d.path.startswith("http") else _public_url(d.path)
        out.append(
            VehicleDocumentOut(
                id=d.id,
                vehicle_id=d.vehicle_id,
                name=d.name,
                filename=d.filename,
                url=url,
                mime_type=d.mime_type,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
        )
    return out


@router.post("/{vehicle_id}/documents", response_model=VehicleDocumentOut)
async def upload_vehicle_document(
    vehicle_id: str,
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> VehicleDocumentOut:
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    if not name.strip():
        raise HTTPException(status_code=400, detail="Document name is required")

    ct = file.content_type or "application/octet-stream"
    allowed_prefixes = ("image/", "application/pdf")
    if not (ct.startswith("image/") or ct == "application/pdf"):
        raise HTTPException(status_code=400, detail="Only images or PDF are allowed")

    content = await file.read()

    # Upload using B2 or local
    url, new_filename, storage = await upload_file_with_prefix(
        content=content,
        original_filename=file.filename or "",
        prefix=vehicle_id,
        content_type=ct,
        folder="vehicles",
        local_subdir="vehicles",
    )

    doc = VehicleDocument(
        vehicle_id=vehicle_id,
        name=name.strip(),
        filename=file.filename or new_filename,
        path=url,
        mime_type=ct,
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    return VehicleDocumentOut(
        id=doc.id,
        vehicle_id=doc.vehicle_id,
        name=doc.name,
        filename=doc.filename,
        url=url,
        mime_type=doc.mime_type,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
    )


@router.delete("/{vehicle_id}/documents/{doc_id}")
async def delete_vehicle_document(vehicle_id: str, doc_id: int, db: Session = Depends(get_db)) -> dict:
    doc = (
        db.query(VehicleDocument)
        .filter(VehicleDocument.id == doc_id)
        .filter(VehicleDocument.vehicle_id == vehicle_id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        if doc.path and not doc.path.startswith("http") and os.path.exists(doc.path):
            os.remove(doc.path)
    except Exception:
        pass

    db.delete(doc)
    db.commit()

    return {"message": "Document deleted"}
