import os
import shutil
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from app.core.database import engine
from app.core.security import get_password_hash
from app.models.core.rbac import Permission, Role
from app.models.core.user import User

def _ensure_client_name_is_text() -> None:
    if engine.dialect.name != "postgresql":
        return

    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE clients ALTER COLUMN client_name TYPE TEXT"))
        except Exception:
            pass

def _seed_rbac() -> None:
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

    users = {
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
        "hr_payroll_accounts": {
            "email": "hr_payroll_accounts@local.com",
            "full_name": "HR Payroll + Accounts",
            "password": "HRPayrollAccounts@123",
            "is_superuser": False,
            "roles": ["HRPayrollAccountsFull"],
        },
    }

    db = Session(bind=engine)
    try:
        def _next_id(model_cls) -> int:
            try:
                cur = db.query(func.max(model_cls.id)).scalar()
                return int(cur or 0) + 1
            except Exception:
                return 1

        for key, desc in permissions.items():
            with db.no_autoflush:
                exists = db.query(Permission).filter(Permission.key == key).first()
            if not exists:
                row = Permission(key=key, description=desc)
                if getattr(row, "id", None) is None:
                    row.id = _next_id(Permission)
                db.add(row)
        db.commit()

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
            r.permissions = [perm_by_key[k] for k in spec.get("permissions", []) if k in perm_by_key]
        db.commit()

        role_by_name = {r.name: r for r in db.query(Role).all()}
        for username, spec in users.items():
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
            else:
                u.email = spec["email"]
                u.full_name = spec.get("full_name")
                u.is_superuser = bool(spec.get("is_superuser", False))
                u.is_active = True
                u.hashed_password = get_password_hash(spec["password"])
            u.roles = [role_by_name[n] for n in spec.get("roles", []) if n in role_by_name]
        db.commit()
    finally:
        db.close()

def _ensure_rbac_id_defaults() -> None:
    if engine.dialect.name != "postgresql":
        return

    with engine.begin() as conn:
        try:
            conn.execute(text("CREATE SEQUENCE IF NOT EXISTS permissions_id_seq"))
            conn.execute(text("ALTER TABLE permissions ALTER COLUMN id SET DEFAULT nextval('permissions_id_seq')"))
            conn.execute(text("SELECT setval('permissions_id_seq', COALESCE((SELECT MAX(id) FROM permissions), 1), true)"))
        except Exception:
            pass

        try:
            conn.execute(text("CREATE SEQUENCE IF NOT EXISTS roles_id_seq"))
            conn.execute(text("ALTER TABLE roles ALTER COLUMN id SET DEFAULT nextval('roles_id_seq')"))
            conn.execute(text("SELECT setval('roles_id_seq', COALESCE((SELECT MAX(id) FROM roles), 1), true)"))
        except Exception:
            pass

        try:
            conn.execute(text("CREATE SEQUENCE IF NOT EXISTS users_id_seq"))
            conn.execute(text("ALTER TABLE users ALTER COLUMN id SET DEFAULT nextval('users_id_seq')"))
            conn.execute(text("SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1), true)"))
        except Exception:
            pass

def _ensure_employee_columns_exist() -> None:
    employee_columns = {
        "agreement": "BOOLEAN DEFAULT 0",
        "police_clearance": "BOOLEAN DEFAULT 0",
        "fingerprint_check": "BOOLEAN DEFAULT 0",
        "background_screening": "BOOLEAN DEFAULT 0",
        "reference_verification": "BOOLEAN DEFAULT 0",
        "guard_card": "BOOLEAN DEFAULT 0",
        "guard_card_doc": "TEXT",
        "police_clearance_doc": "TEXT",
        "fingerprint_check_doc": "TEXT",
        "background_screening_doc": "TEXT",
        "reference_verification_doc": "TEXT",
        "total_salary": "VARCHAR",
        "account_type": "VARCHAR",
        "bank_accounts": "TEXT",
        "languages_spoken": "TEXT",
        "languages_proficiency": "TEXT",
        "height_cm": "INTEGER",
        "permanent_address": "TEXT",
        "temporary_address": "TEXT",
        "cnic": "VARCHAR",
        "cnic_expiry_date": "VARCHAR",
        "domicile": "VARCHAR",
        "personal_phone_number": "VARCHAR",
        "next_of_kin_cnic": "VARCHAR",
        "next_of_kin_mobile_number": "VARCHAR",
        "permanent_village": "VARCHAR",
        "permanent_post_office": "VARCHAR",
        "permanent_thana": "VARCHAR",
        "permanent_tehsil": "VARCHAR",
        "permanent_district": "VARCHAR",
        "present_village": "VARCHAR",
        "present_post_office": "VARCHAR",
        "present_thana": "VARCHAR",
        "present_tehsil": "VARCHAR",
        "present_district": "VARCHAR",
        "enrolled_as": "VARCHAR",
        "interviewed_by": "VARCHAR",
        "introduced_by": "VARCHAR",
        "retired_from": "TEXT",
        "service_unit": "VARCHAR",
        "service_rank": "VARCHAR",
        "service_enrollment_date": "VARCHAR",
        "service_reenrollment_date": "VARCHAR",
        "medical_category": "VARCHAR",
        "discharge_cause": "TEXT",
        "blood_group": "VARCHAR",
        "civil_education_type": "VARCHAR",
        "civil_education_detail": "VARCHAR",
        "sons_names": "TEXT",
        "daughters_names": "TEXT",
        "brothers_names": "TEXT",
        "sisters_names": "TEXT",
        "particulars_verified_by_sho_on": "VARCHAR",
        "particulars_verified_by_ssp_on": "VARCHAR",
        "police_khidmat_verification_on": "VARCHAR",
        "signature_recording_officer": "TEXT",
        "signature_individual": "TEXT",
        "fss_number": "VARCHAR",
        "fss_name": "VARCHAR",
        "fss_so": "VARCHAR",
        "original_doc_held": "TEXT",
        "documents_handed_over_to": "VARCHAR",
        "photo_on_document": "VARCHAR",
        "eobi_no": "VARCHAR",
        "insurance": "VARCHAR",
        "social_security": "VARCHAR",
        "home_contact_no": "VARCHAR",
        "police_training_letter_date": "VARCHAR",
        "vaccination_certificate": "VARCHAR",
        "volume_no": "VARCHAR",
        "payments": "TEXT",
        "fingerprint_attested_by": "VARCHAR",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(employees)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='employees'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in employee_columns.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE employees ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def _ensure_employee_warning_columns_exist() -> None:
    cols = {
        "found_with": "TEXT",
        "supervisor_signature": "VARCHAR",
        "supervisor_signature_date": "VARCHAR",
        "notice_text": "TEXT",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(employee_warnings)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='employee_warnings'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in cols.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE employee_warnings ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def _ensure_client_site_guard_allocation_employee_fk() -> None:
    if engine.dialect.name != "postgresql":
        return

    with engine.begin() as conn:
        try:
            conn.execute(
                text(
                    "ALTER TABLE client_site_guard_allocations "
                    "DROP CONSTRAINT IF EXISTS client_site_guard_allocations_employee_db_id_fkey"
                )
            )
            conn.execute(
                text(
                    "ALTER TABLE client_site_guard_allocations "
                    "ADD CONSTRAINT client_site_guard_allocations_employee_db_id_fkey "
                    "FOREIGN KEY (employee_db_id) REFERENCES employees2(id)"
                )
            )
        except Exception:
            pass

def _ensure_employee2_attachment_columns_exist() -> None:
    cols = {
        "recording_officer_signature_attachment": "TEXT",
        "experience_security_attachment": "TEXT",
        "education_attachment": "TEXT",
        "nok_cnic_attachment": "TEXT",
        "other_documents_attachment": "TEXT",
        "address_details": "TEXT",
        "temp_village": "TEXT",
        "temp_post_office": "TEXT",
        "temp_thana": "TEXT",
        "temp_tehsil": "TEXT",
        "temp_district": "TEXT",
        "temp_city": "TEXT",
        "temp_phone": "TEXT",
        "temp_address_details": "TEXT",
        "insurance": "TEXT",
        "social_security": "TEXT",
        "designation": "TEXT",
        "allocation_status": "TEXT",
        "avatar_url": "TEXT",
        "cnic_attachment": "TEXT",
        "domicile_attachment": "TEXT",
        "sho_verified_attachment": "TEXT",
        "ssp_verified_attachment": "TEXT",
        "khidmat_verified_attachment": "TEXT",
        "police_trg_attachment": "TEXT",
        "photo_on_doc_attachment": "TEXT",
        "personal_signature_attachment": "TEXT",
        "fingerprint_thumb_attachment": "TEXT",
        "fingerprint_index_attachment": "TEXT",
        "fingerprint_middle_attachment": "TEXT",
        "fingerprint_ring_attachment": "TEXT",
        "fingerprint_pinky_attachment": "TEXT",
        "employment_agreement_attachment": "TEXT",
        "served_in_attachment": "TEXT",
        "vaccination_attachment": "TEXT",
        "bank_accounts": "TEXT",
        "height": "TEXT",
        "education": "TEXT",
        "medical_category": "TEXT",
        "medical_details": "TEXT",
        "medical_discharge_cause": "TEXT",
        "nok_name": "TEXT",
        "nok_relationship": "TEXT",
        "sons_count": "TEXT",
        "daughters_count": "TEXT",
        "brothers_count": "TEXT",
        "sisters_count": "TEXT",
        "interviewed_by": "TEXT",
        "introduced_by": "TEXT",
        "enrolled_as": "TEXT",
        "served_in": "TEXT",
        "experience_security": "TEXT",
        "deployment_details": "TEXT",
        "dod": "TEXT",
        "discharge_cause": "TEXT",
        "orig_docs_received": "TEXT",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(employees2)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='employees2'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in cols.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE employees2 ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def _ensure_general_item_columns_exist() -> None:
    cols = {
        "image_url": "VARCHAR",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(general_items)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='general_items'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in cols.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE general_items ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def _ensure_client_guard_requirement_columns_exist() -> None:
    cols = {
        "start_date": "DATE",
        "end_date": "DATE",
        "preferred_language": "VARCHAR",
        "monthly_amount": "FLOAT",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(client_guard_requirements)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='client_guard_requirements'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in cols.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE client_guard_requirements ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def _ensure_attendance_columns_exist() -> None:
    attendance_columns = {
        "overtime_minutes": "INTEGER",
        "overtime_rate": "FLOAT",
        "late_minutes": "INTEGER",
        "late_deduction": "FLOAT",
        "leave_type": "VARCHAR",
        "fine_amount": "FLOAT",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(attendance_records)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='attendance_records'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in attendance_columns.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE attendance_records ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def _ensure_vehicle_columns_exist() -> None:
    vehicle_columns = {
        "chassis_number": "VARCHAR(100)",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(vehicles)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='vehicles'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in vehicle_columns.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE vehicles ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def _ensure_vehicle_assignment_columns_exist() -> None:
    assignment_columns = {
        "route_stops": "TEXT",
        "status": "VARCHAR(30) DEFAULT 'Incomplete'",
        "assignment_date": "DATE",
        "distance_km": "FLOAT",
        "rate_per_km": "FLOAT",
        "amount": "FLOAT",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(vehicle_assignments)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='vehicle_assignments'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in assignment_columns.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE vehicle_assignments ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def _ensure_payroll_payment_status_columns_exist() -> None:
    payroll_columns = {
        "employee_db_id": "INTEGER",
        "net_pay_snapshot": "FLOAT",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(payroll_payment_status)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='payroll_payment_status'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in payroll_columns.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE payroll_payment_status ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def _ensure_payroll_sheet_entry_columns_exist() -> None:
    cols = {
        "ot_rate_override": "FLOAT DEFAULT 0.0",
        "ot_bonus_amount": "FLOAT DEFAULT 0.0",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(payroll_sheet_entries)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='payroll_sheet_entries'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in cols.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE payroll_sheet_entries ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def _ensure_payroll_sheet_entry_employee_fk() -> None:
    if engine.dialect.name != "postgresql":
        return

    with engine.begin() as conn:
        try:
            conn.execute(
                text(
                    "ALTER TABLE payroll_sheet_entries "
                    "DROP CONSTRAINT IF EXISTS payroll_sheet_entries_employee_db_id_fkey"
                )
            )
            conn.execute(
                text(
                    "ALTER TABLE payroll_sheet_entries "
                    "ADD CONSTRAINT payroll_sheet_entries_employee_db_id_fkey "
                    "FOREIGN KEY (employee_db_id) REFERENCES employees2(id)"
                )
            )
        except Exception:
            pass

def _ensure_client_site_guard_allocation_columns_exist() -> None:
    cols = {
        "site_id": "INTEGER",
        "contract_id": "INTEGER",
        "requirement_id": "INTEGER",
        "employee_db_id": "INTEGER",
        "start_date": "DATE",
        "end_date": "DATE",
        "status": "VARCHAR(30) DEFAULT 'Allocated'",
    }

    with engine.begin() as conn:
        try:
            existing = set()
            if engine.dialect.name == "sqlite":
                rows = conn.execute(text("PRAGMA table_info(client_site_guard_allocations)")).fetchall()
                existing = {r[1] for r in rows}
            else:
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='client_site_guard_allocations'"
                    )
                ).fetchall()
                existing = {r[0] for r in rows}

            for col, ddl in cols.items():
                if col in existing:
                    continue
                conn.execute(text(f"ALTER TABLE client_site_guard_allocations ADD COLUMN {col} {ddl}"))
        except Exception:
            pass

def migrate_legacy_uploads(uploads_dir: str):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Assuming app/core/startup_tasks.py -> up 2 levels is app/
    # uploads_dir is passed from main.py
    
    _legacy_dirs = [
        os.path.join(base_dir, "uploads"),
        os.path.join(os.path.dirname(base_dir), "uploads")
    ]
    
    try:
        target_vehicles = os.path.join(uploads_dir, "vehicles")
        os.makedirs(target_vehicles, exist_ok=True)
        for _legacy_uploads_dir in _legacy_dirs:
            legacy_vehicles = os.path.join(_legacy_uploads_dir, "vehicles")
            if not os.path.isdir(legacy_vehicles):
                continue
            for fn in os.listdir(legacy_vehicles):
                src = os.path.join(legacy_vehicles, fn)
                dst = os.path.join(target_vehicles, fn)
                if os.path.isfile(src) and not os.path.exists(dst):
                    shutil.copy2(src, dst)
    except Exception:
        pass

def run_startup_tasks():
    _ensure_rbac_id_defaults()
    try:
        _seed_rbac()
    except Exception:
        pass

    _ensure_client_name_is_text()
    _ensure_employee_columns_exist()
    _ensure_employee_warning_columns_exist()
    _ensure_client_site_guard_allocation_employee_fk()
    _ensure_employee2_attachment_columns_exist()
    _ensure_general_item_columns_exist()
    _ensure_client_guard_requirement_columns_exist()
    _ensure_attendance_columns_exist()
    _ensure_vehicle_columns_exist()
    _ensure_vehicle_assignment_columns_exist()
    _ensure_payroll_payment_status_columns_exist()
    _ensure_payroll_sheet_entry_columns_exist()
    _ensure_payroll_sheet_entry_employee_fk()
    _ensure_client_site_guard_allocation_columns_exist()
