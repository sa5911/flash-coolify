# Alembic - Database Migrations

## Overview
Alembic manages database schema migrations for this project.

## Common Commands
```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## Migration Files
Located in `alembic/versions/`. Each file represents a schema change.

## Configuration
- `alembic.ini`: Alembic configuration
- `alembic/env.py`: Migration environment setup
