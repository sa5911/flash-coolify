````markdown
# Flash ERP Backend

FastAPI-based backend for Flash ERP system with PostgreSQL database.

## Features

- FastAPI REST API
- PostgreSQL database with SQLAlchemy ORM
- JWT authentication
- Role-based access control (RBAC)
- Employee management
- Attendance tracking
- Payroll system
- Fleet management
- Client management
- Inventory management
- Finance & accounting

## Requirements

- Python 3.10+
- PostgreSQL 12+

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd backend-flash-dockpoly
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Application
APP_NAME=Flash ERP
APP_VERSION=1.0.0
DEBUG=False
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Default Users

After first startup, the following users are created:

- **Super Admin**: superadmin@local.com / SuperAdmin@123
- **Employee Entry**: employee_entry@local.com / Employee@123
- **Attendance Manager**: attendance_manager@local.com / Attendance@123
- **HR Payroll**: hr_payroll@local.com / HRPayroll@123

## Deployment

### Docker

```bash
docker build -t flash-erp-backend .
docker run -p 8000:8000 --env-file .env flash-erp-backend
```

### Dokploy / Railway / Render

1. Set environment variables in your platform
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## License

Proprietary

````
