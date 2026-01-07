import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import api_router
from app.core.startup_tasks import run_startup_tasks, migrate_legacy_uploads
import fastadmin
import app.models  # Import models to create tables

# Create database tables
Base.metadata.create_all(bind=engine)

# Run startup tasks (migrations, seeding, checks)
run_startup_tasks()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A modern ERP system built with FastAPI and React",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials="*" not in settings.allowed_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to ensure CORS headers are sent even on 500 errors."""
    import traceback
    traceback.print_exc()
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=500,
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Credentials": "true",
        },
    )

# Include API router
app.include_router(api_router, prefix="/api")

# Include fastadmin router
app.include_router(fastadmin.api.frameworks.fastapi.app.api_router, prefix="/admin")

# Serve uploads from project root so previously uploaded files remain accessible.
_uploads_dir = os.path.abspath(settings.UPLOADS_DIR)
os.makedirs(_uploads_dir, exist_ok=True)

# Migrate legacy uploads
migrate_legacy_uploads(_uploads_dir)

app.mount("/uploads", StaticFiles(directory=_uploads_dir), name="uploads")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "unhealthy", "detail": str(e)})
