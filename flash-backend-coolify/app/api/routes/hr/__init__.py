from .router import router
from .documents import router as documents_router
from .warnings import router as warnings_router
from .attendance import router as attendance_router
from .leave_periods import router as leave_periods_router
from .payroll import router as payroll_router
from .payroll2 import router as payroll2_router
from .inactive import router as inactive_router
from .employees2 import router as employees2_router
from .advances import router as advances_router

# Combine all sub-routers into the main employees router
router.include_router(documents_router)
router.include_router(warnings_router)
router.include_router(attendance_router)
router.include_router(leave_periods_router)
router.include_router(payroll_router)
router.include_router(payroll2_router)
router.include_router(inactive_router)
router.include_router(employees2_router)
# Advances router is mounted separately

__all__ = ["router"]
