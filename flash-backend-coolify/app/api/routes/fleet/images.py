import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.upload_helper import upload_file_with_prefix
from app.models.fleet.vehicle import Vehicle
from app.models.fleet.vehicle_image import VehicleImage
from app.schemas.fleet.vehicle_image import VehicleImageOut


router = APIRouter()


def _upload_dir() -> str:
    d = os.path.join(os.path.abspath(settings.UPLOADS_DIR), "vehicles", "images")
    os.makedirs(d, exist_ok=True)
    return d


def _public_url(path: str) -> str:
    fn = os.path.basename(path)
    return f"/uploads/vehicles/images/{fn}"


@router.get("/{vehicle_id}/images", response_model=List[VehicleImageOut])
async def list_vehicle_images(vehicle_id: str, db: Session = Depends(get_db)) -> List[VehicleImageOut]:
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    imgs = (
        db.query(VehicleImage)
        .filter(VehicleImage.vehicle_id == vehicle_id)
        .order_by(VehicleImage.id.desc())
        .all()
    )

    out: List[VehicleImageOut] = []
    for img in imgs:
        url = img.path if img.path.startswith("http") else _public_url(img.path)
        out.append(
            VehicleImageOut(
                id=img.id,
                vehicle_id=img.vehicle_id,
                filename=img.filename,
                url=url,
                mime_type=img.mime_type,
                created_at=img.created_at,
                updated_at=img.updated_at,
            )
        )
    return out


@router.post("/{vehicle_id}/images", response_model=VehicleImageOut)
async def upload_vehicle_image(
    vehicle_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> VehicleImageOut:
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    ct = file.content_type or "application/octet-stream"
    if not ct.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    content = await file.read()

    # Upload using B2 or local
    url, new_filename, storage = await upload_file_with_prefix(
        content=content,
        original_filename=file.filename or "",
        prefix=vehicle_id,
        content_type=ct,
        folder="vehicles/images",
        local_subdir="vehicles/images",
    )

    img = VehicleImage(
        vehicle_id=vehicle_id,
        filename=file.filename or new_filename,
        path=url,
        mime_type=ct,
    )

    db.add(img)
    db.commit()
    db.refresh(img)

    return VehicleImageOut(
        id=img.id,
        vehicle_id=img.vehicle_id,
        filename=img.filename,
        url=url,
        mime_type=img.mime_type,
        created_at=img.created_at,
        updated_at=img.updated_at,
    )


@router.delete("/{vehicle_id}/images/{image_id}")
async def delete_vehicle_image(vehicle_id: str, image_id: int, db: Session = Depends(get_db)) -> dict:
    img = (
        db.query(VehicleImage)
        .filter(VehicleImage.id == image_id)
        .filter(VehicleImage.vehicle_id == vehicle_id)
        .first()
    )
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        if img.path and not img.path.startswith("http") and os.path.exists(img.path):
            os.remove(img.path)
    except Exception:
        pass

    db.delete(img)
    db.commit()

    return {"message": "Image deleted"}
