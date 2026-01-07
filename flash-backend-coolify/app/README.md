# App Module

## Overview
Main application module containing all business logic, APIs, models, and schemas.

## Structure
```
app/
├── main.py              # FastAPI application entry point
├── core/                # Core infrastructure (config, db, auth)
├── api/                 # API routes organized by domain
│   └── routes/
│       ├── client/      # Client management APIs
│       ├── finance/     # Financial APIs
│       ├── fleet/       # Fleet management APIs
│       ├── hr/          # HR and payroll APIs
│       ├── inventory/   # Inventory APIs
│       └── core/        # Auth, users, RBAC, uploads
├── models/              # SQLAlchemy database models
└── schemas/             # Pydantic validation schemas
```

## Domain Separation
The application is organized by business domain (Client, Finance, Fleet, HR, Inventory). Each domain has its own:
- API routes (`api/routes/{domain}/`)
- Database models (`models/{domain}/`)
- Pydantic schemas (`schemas/{domain}/`)

This separation makes the codebase easier to navigate and maintain.
