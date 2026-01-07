# Core Module

## Overview
The Core module provides foundational services and shared utilities for the entire application. It handles authentication, database connections, security, and global configuration.

## Key Components
- **Auth**: JWT-based authentication and user session management.
- **Database**: Database connection pooling and session management (SQLAlchemy).
- **Config**: Global application settings and environment variable handling.
- **Uploads**: File upload handling with local storage support.
- **RBAC**: Role-Based Access Control system.

## Dependencies
- `app.models.core`: User, Role, Permission details.
- `app.core.config`: Settings.
