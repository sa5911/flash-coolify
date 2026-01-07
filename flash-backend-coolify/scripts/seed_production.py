#!/usr/bin/env python3
"""
Seed script for production PostgreSQL database.

This script:
1. Creates all database tables (if not exist)
2. Seeds permissions and roles
3. Creates default users including superadmin

Usage:
  Set DATABASE_URL environment variable to your PostgreSQL connection string, then run:
  python seed_production.py

  Or run with environment variable inline:
  DATABASE_URL="postgresql://..." python seed_production.py
"""

import os
import sys

# Ensure app is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy import func

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set.")
    print("Please set it to your PostgreSQL connection string.")
    print("Example: postgresql://user:password@host:5432/database")
    sys.exit(1)

# Convert postgres:// to postgresql:// for SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Connecting to database...")
print(f"URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'configured'}")

engine = create_engine(DATABASE_URL)

# Import models
from flash_backend.core.database import Base
from flash_backend.core.security import get_password_hash
from flash_backend.models.user import User
from flash_backend.models.rbac import Permission, Role

# Import all models to register them with Base
from flash_backend.models import (
    user, vehicle, vehicle_document, vehicle_image, fuel_entry,
    employee, employee_document, employee_warning, employee_warning_document,
    attendance, leave_period, vehicle_assignment, vehicle_maintenance,
    payroll_payment_status, payroll_sheet_entry, employee_advance,
    employee_advance_deduction, general_item, general_item_transaction,
    general_item_employee_balance, client, client_contact, client_address,
    client_site, client_contract, client_guard_requirement,
    client_site_guard_allocation, client_rate_card, client_invoice,
    client_document, restricted_item, restricted_item_image,
    restricted_item_serial_unit, restricted_item_transaction,
    restricted_item_employee_balance, finance_account, finance_journal_line,
    finance_journal_entry, expense, employee2,
)

def create_tables():
    """Create all database tables."""
    print("\n1. Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("   ✓ Tables created successfully")

def seed_rbac():
    """Seed permissions, roles, and users."""
    print("\n2. Seeding RBAC (Permissions, Roles, Users)...")
    
    permissions = {
        "employees:view": "View employees",
        "employees:create": "Create employees",
        "employees:update": "Update employees",
        "employees:delete": "Delete employees",
        "attendance:manage": "View and manage attendance",
        "payroll:view": "View payroll",
        "performance:view": "View performance dashboards",
        "clients:view": "View client management",
        "fleet:view": "View fleet module",
        "inventory:view": "View inventory module",
        "accounts:full": "Full access to accounts/finance/expenses/advances/exports",
        "rbac:admin": "Manage roles/permissions/users",
    }

    roles = {
        "SuperAdmin": {
            "description": "System super admin role",
            "is_system": True,
            "permissions": list(permissions.keys()),
        },
        "EmployeeEntry": {
            "description": "Can create employees",
            "is_system": True,
            "permissions": ["employees:create", "employees:view", "employees:update"],
        },
        "AttendanceManager": {
            "description": "Can view and manage attendance",
            "is_system": True,
            "permissions": ["attendance:manage", "employees:view"],
        },
        "HRPayrollViewer": {
            "description": "Can view attendance and payroll",
            "is_system": True,
            "permissions": ["attendance:manage", "payroll:view", "employees:view"],
        },
        "ClientsViewer": {
            "description": "Can view clients section",
            "is_system": True,
            "permissions": ["clients:view"],
        },
        "AccountsFull": {
            "description": "Full access to accounts section",
            "is_system": True,
            "permissions": ["accounts:full"],
        },
        "HRPayrollAccountsFull": {
            "description": "Attendance + Payroll + full accounts",
            "is_system": True,
            "permissions": ["attendance:manage", "payroll:view", "accounts:full", "employees:view"],
        },
    }

    users_data = {
        "superadmin": {
            "email": "superadmin@local.com",
            "full_name": "Super Admin",
            "password": "SuperAdmin@123",
            "is_superuser": True,
            "roles": ["SuperAdmin"],
        },
        "employee_entry": {
            "email": "employee_entry@local.com",
            "full_name": "Employee Entry",
            "password": "Employee@123",
            "is_superuser": False,
            "roles": ["EmployeeEntry"],
        },
        "attendance_manager": {
            "email": "attendance_manager@local.com",
            "full_name": "Attendance Manager",
            "password": "Attendance@123",
            "is_superuser": False,
            "roles": ["AttendanceManager"],
        },
        "hr_payroll": {
            "email": "hr_payroll@local.com",
            "full_name": "HR Payroll",
            "password": "HRPayroll@123",
            "is_superuser": False,
            "roles": ["HRPayrollViewer"],
        },
        "clients_view": {
            "email": "clients_view@local.com",
            "full_name": "Clients Viewer",
            "password": "Clients@123",
            "is_superuser": False,
            "roles": ["ClientsViewer"],
        },
        "accounts_full": {
            "email": "accounts_full@local.com",
            "full_name": "Accounts Full",
            "password": "Accounts@123",
            "is_superuser": False,
            "roles": ["AccountsFull"],
        },
    }

    db = Session(bind=engine)
    try:
        def _next_id(model_cls):
            try:
                cur = db.query(func.max(model_cls.id)).scalar()
                return int(cur or 0) + 1
            except Exception:
                return 1

        # Seed permissions
        print("   Creating permissions...")
        for key, desc in permissions.items():
            with db.no_autoflush:
                exists = db.query(Permission).filter(Permission.key == key).first()
            if not exists:
                row = Permission(key=key, description=desc)
                if getattr(row, "id", None) is None:
                    row.id = _next_id(Permission)
                db.add(row)
                print(f"      + {key}")
        db.commit()

        # Seed roles
        print("   Creating roles...")
        perm_by_key = {p.key: p for p in db.query(Permission).all()}
        for role_name, spec in roles.items():
            with db.no_autoflush:
                r = db.query(Role).filter(Role.name == role_name).first()
            if not r:
                r = Role(
                    id=_next_id(Role),
                    name=role_name,
                    description=spec.get("description"),
                    is_system=bool(spec.get("is_system", False)),
                )
                db.add(r)
                db.flush()
                print(f"      + {role_name}")
            r.permissions = [perm_by_key[k] for k in spec.get("permissions", []) if k in perm_by_key]
        db.commit()

        # Seed users
        print("   Creating users...")
        role_by_name = {r.name: r for r in db.query(Role).all()}
        for username, spec in users_data.items():
            with db.no_autoflush:
                u = db.query(User).filter(User.username == username).first()
            if not u:
                u = User(
                    id=_next_id(User),
                    email=spec["email"],
                    username=username,
                    full_name=spec.get("full_name"),
                    hashed_password=get_password_hash(spec["password"]),
                    is_active=True,
                    is_superuser=bool(spec.get("is_superuser", False)),
                )
                db.add(u)
                db.flush()
                print(f"      + {username} (password: {spec['password']})")
            else:
                u.email = spec["email"]
                u.full_name = spec.get("full_name")
                u.is_superuser = bool(spec.get("is_superuser", False))
                u.is_active = True
                u.hashed_password = get_password_hash(spec["password"])
                print(f"      ~ {username} (updated)")
            u.roles = [role_by_name[n] for n in spec.get("roles", []) if n in role_by_name]
        db.commit()

        print("   ✓ RBAC seeded successfully")
    finally:
        db.close()

def ensure_sequences():
    """Ensure PostgreSQL sequences are set up correctly."""
    if engine.dialect.name != "postgresql":
        return

    print("\n3. Setting up PostgreSQL sequences...")
    
    with engine.begin() as conn:
        sequences = [
            ("permissions", "permissions_id_seq"),
            ("roles", "roles_id_seq"),
            ("users", "users_id_seq"),
        ]
        
        for table, seq in sequences:
            try:
                conn.execute(text(f"CREATE SEQUENCE IF NOT EXISTS {seq}"))
                conn.execute(text(f"ALTER TABLE {table} ALTER COLUMN id SET DEFAULT nextval('{seq}')"))
                conn.execute(text(f"SELECT setval('{seq}', COALESCE((SELECT MAX(id) FROM {table}), 1), true)"))
                print(f"   ✓ {seq} configured")
            except Exception as e:
                print(f"   ! {seq}: {e}")

def main():
    print("=" * 60)
    print("Flash ERP - Production Database Seed Script")
    print("=" * 60)
    
    try:
        create_tables()
        ensure_sequences()
        seed_rbac()
        
        print("\n" + "=" * 60)
        print("✅ Database seeding completed successfully!")
        print("=" * 60)
        print("\n📋 Default Login Credentials:")
        print("-" * 40)
        print("SuperAdmin:")
        print("   Username: superadmin")
        print("   Password: SuperAdmin@123")
        print("-" * 40)
        print("\nOther users available:")
        print("   - employee_entry / Employee@123")
        print("   - attendance_manager / Attendance@123")
        print("   - hr_payroll / HRPayroll@123")
        print("   - clients_view / Clients@123")
        print("   - accounts_full / Accounts@123")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
