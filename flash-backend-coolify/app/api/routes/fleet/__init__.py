from .router import router
from .documents import router as documents_router
from .images import router as images_router
from .assignments import router as assignments_router
from .maintenance import router as maintenance_router
from .fuel import router as fuel_router

# Combine all sub-routers into the main router
router.include_router(documents_router)
router.include_router(images_router)
router.include_router(assignments_router)
router.include_router(maintenance_router)
# Fuel router is mounted separately in app/main.py / app/api/routes/__init__.py

__all__ = ["router"]
