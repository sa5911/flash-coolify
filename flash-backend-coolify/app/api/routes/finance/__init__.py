from .router import router
from .expenses import router as expenses_router
from .exports import router as exports_router

# Combine sub-routers?
# Previously finance.router might have been standalone.
# But I moved exports and expenses into finance folder.
# 'router.py' (was finance.py) likely defines routes.
# 'expenses.py' defines routes.
# In app/api/routes/__init__.py, I included them separately:
# api_router.include_router(finance_router, prefix="/finance")
# api_router.include_router(expenses.router, prefix="/expenses")
# api_router.include_router(exports.router, prefix="/exports")

# So I don't need to combine them here. Just export them.
# But 'router' variable typically implies the main router of the package.
# app/api/routes/__init__.py imports 'router' from 'finance'.
# That 'router' corresponds to 'finance.py' router.

__all__ = ["router", "expenses_router", "exports_router"]
