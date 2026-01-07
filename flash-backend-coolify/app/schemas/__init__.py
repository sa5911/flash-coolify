"""Schemas package initialization."""

from app.schemas.core.user import (
    User,
    UserCreate,
    UserUpdate,
    UserInDB,
    Token,
    TokenData,
)
from app.schemas.fleet.vehicle import (
    VehicleBase,
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
)
from app.schemas.fleet.vehicle_image import VehicleImageOut
from app.schemas.fleet.vehicle_maintenance import VehicleMaintenanceCreate, VehicleMaintenanceResponse, VehicleMaintenanceUpdate
from app.schemas.hr.employee_document import EmployeeDocumentOut

__all__ = [
    "User",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "Token",
    "TokenData",
    "VehicleBase",
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleResponse",
]
