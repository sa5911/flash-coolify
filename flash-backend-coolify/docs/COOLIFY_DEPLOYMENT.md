````markdown
# Coolify Deployment Guide - Flash ERP Backend

This guide will help you deploy the Flash ERP Backend on Coolify using Nixpacks.

## Prerequisites

- Coolify instance running
- GitHub repository: `https://github.com/flashtechdeploy-prod/flash-backend-coolify`
- PostgreSQL database (can be created in Coolify)

## Deployment Steps

### 1. Create PostgreSQL Database in Coolify

1. Go to your Coolify dashboard
2. Click **"+ New Resource"** → **"Database"** → **"PostgreSQL"**
3. Configure:
   - Name: `flash-erp-db`
   - Version: PostgreSQL 17 (or latest)
   - Username: `postgres` (default)
   - Password: (auto-generated or set your own)
4. Click **"Create"**
5. **Copy the connection string** - you'll need it for environment variables

### 2. Create New Application

1. In Coolify, click **"+ New Resource"** → **"Application"**
2. Choose **"Public Repository"**
3. Enter repository URL: `https://github.com/flashtechdeploy-prod/flash-backend-coolify`
4. Branch: `main`
5. Click **"Continue"**

### 3. Configure Build Settings

Coolify should auto-detect Nixpacks. Verify:

- **Build Pack**: Nixpacks (auto-detected from `nixpacks.toml`)
- **Install Command**: `pip install -r requirements.txt` (auto-detected)
- **Build Command**: (leave empty or `mkdir -p uploads`)
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 4. Set Environment Variables

In the **Environment Variables** section, add:

```env
# Database (use your Coolify PostgreSQL connection string)
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@postgres-service:5432/postgres?sslmode=require

# Security (generate a secure random key)
SECRET_KEY=your-super-secret-key-change-this-min-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (add your frontend domain)
ALLOWED_ORIGINS=https://your-frontend-domain.com,http://localhost:3000

# Application
APP_NAME=Flash ERP
APP_VERSION=1.0.0
DEBUG=False

# Port (Coolify sets this automatically)
PORT=8000
```

**Important Notes:**

- Replace `YOUR_PASSWORD` with your PostgreSQL password
- Replace `postgres-service` with your actual PostgreSQL service name in Coolify
- Generate a secure `SECRET_KEY` (32+ characters)
- Update `ALLOWED_ORIGINS` with your actual frontend URL

### 5. Configure Networking

1. **Port**: Coolify will automatically expose port `8000`
2. **Domain**:
   - Click **"Add Domain"**
   - Enter your domain (e.g., `api.yourdomain.com`)
   - Enable **"Generate SSL Certificate"** for HTTPS

### 6. Deploy

1. Click **"Deploy"** button
2. Monitor the build logs
3. Wait for deployment to complete (usually 2-5 minutes)

### 7. Verify Deployment

Once deployed, test your API:

```bash
# Health check
curl https://your-api-domain.com/

# API Documentation
https://your-api-domain.com/docs
```

Expected response:

```json
{
  "message": "Welcome to Flash ERP",
  "version": "1.0.0",
  "docs": "/docs"
}
```

## Nixpacks Configuration

The repository includes `nixpacks.toml` which tells Coolify how to build and run the app:

```toml
# Nixpacks configuration for Coolify deployment
providers = ["python"]

[variables]
NIXPACKS_PYTHON_VERSION = "3.11"
PIP_NO_CACHE_DIR = "1"

[phases.setup]
nixPkgs = ["python311", "postgresql", "gcc"]
aptPkgs = ["libpq-dev", "build-essential"]

[phases.install]
cmds = [
    "pip install --upgrade pip setuptools wheel",
    "pip install -r requirements.txt"
]

[phases.build]
cmds = ["mkdir -p uploads"]

[start]
cmd = "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
```

## Troubleshooting

### Build Fails

**Issue**: Dependencies installation fails
**Solution**: Check that `requirements.txt` is in the root directory

**Issue**: Python version mismatch
**Solution**: Verify `nixpacks.toml` specifies `python311`

### Database Connection Fails

**Issue**: Cannot connect to PostgreSQL
**Solution**:

1. Verify `DATABASE_URL` format
2. Check PostgreSQL service is running in Coolify
3. Ensure network connectivity between services
4. Use internal service name (e.g., `postgres-service:5432`)

### Application Won't Start

**Issue**: Port binding error
**Solution**: Ensure start command uses `$PORT` variable

**Issue**: Missing environment variables
**Solution**: Verify all required env vars are set in Coolify

### SSL/HTTPS Issues

**Issue**: SSL certificate not working
**Solution**:

1. Ensure domain DNS points to Coolify server
2. Wait for certificate generation (can take a few minutes)
3. Check Coolify logs for certificate errors

## Post-Deployment

### Access API Documentation

Visit: `https://your-api-domain.com/docs`

### Default Admin Login

- Email: `superadmin@local.com`
- Password: `SuperAdmin@123`

**⚠️ IMPORTANT**: Change the default password immediately after first login!

### Monitor Logs

In Coolify dashboard:

1. Go to your application
2. Click **"Logs"** tab
3. Monitor real-time application logs

### Update Deployment

To deploy updates:

1. Push changes to GitHub
2. In Coolify, click **"Redeploy"**
3. Or enable **"Auto Deploy"** for automatic deployments on git push

## Database Migrations

If you need to run Alembic migrations:

1. In Coolify, go to your application
2. Click **"Terminal"** or **"Execute Command"**
3. Run:

```bash
alembic upgrade head
```

## Scaling

To scale your application:

1. Go to application settings in Coolify
2. Adjust **"Replicas"** count
3. Configure load balancing if needed

## Backup

### Database Backup

In Coolify PostgreSQL service:

1. Go to database settings
2. Enable **"Automatic Backups"**
3. Set backup schedule

### Manual Backup

```bash
# In Coolify terminal
pg_dump $DATABASE_URL > backup.sql
```

## Support

- Repository: https://github.com/flashtechdeploy-prod/flash-backend-coolify
- Coolify Docs: https://coolify.io/docs
- Nixpacks Docs: https://nixpacks.com/docs

## Environment Variables Reference

| Variable                    | Required | Description                       | Example                                 |
| --------------------------- | -------- | --------------------------------- | --------------------------------------- |
| DATABASE_URL                | Yes      | PostgreSQL connection string      | `postgresql://user:pass@host:5432/db`   |
| SECRET_KEY                  | Yes      | JWT secret key (32+ chars)        | `your-secret-key-here`                  |
| ALGORITHM                   | Yes      | JWT algorithm                     | `HS256`                                 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Yes      | Token expiration time             | `30`                                    |
| ALLOWED_ORIGINS             | Yes      | CORS allowed origins              | `https://app.com,http://localhost:3000` |
| APP_NAME                    | No       | Application name                  | `Flash ERP`                             |
| APP_VERSION                 | No       | Application version               | `1.0.0`                                 |
| DEBUG                       | No       | Debug mode                        | `False`                                 |
| PORT                        | Auto     | Application port (set by Coolify) | `8000`                                  |

---

**Ready to deploy!** 🚀

````
