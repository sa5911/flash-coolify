from fastapi import APIRouter
from .assignments import router as assignments_router
from .general import router as general_router
from .restricted import router as restricted_router

# Create a composite router for the package
router = APIRouter()
router.include_router(assignments_router)
router.include_router(general_router)
router.include_router(restricted_router)

__all__ = ["router"]
