import os
import shutil

base_dir = r"c:\Users\HomePC\Desktop\app\flash-backend-coolify\app\api\routes"

# 1. Rename directories
renames = {
    "vehicles": "fleet",
    "employees": "hr",
    "client_management": "client"
}

for old, new in renames.items():
    old_path = os.path.join(base_dir, old)
    new_path = os.path.join(base_dir, new)
    if os.path.exists(old_path) and not os.path.exists(new_path):
        try:
            shutil.move(old_path, new_path)
            print(f"Renamed {old} to {new}")
        except Exception as e:
            print(f"Error renaming {old}: {e}")

# 2. Move files
# Target: (Source, DestinationFilename)
moves = {
    "fleet": [
        ("fuel_entries.py", "fuel.py") 
    ],
    "inventory": [
        ("general_inventory.py", "general.py"),
        ("restricted_inventory.py", "restricted.py"),
        ("inventory_assignments.py", "assignments.py")
    ],
    "finance": [
        ("finance.py", "router.py"),
        ("expenses.py", "expenses.py"),
        ("exports_accounts.py", "exports.py")
    ],
    "hr": [
        ("hr.py", "analytics_hr.py") # Renamed to avoid confusion with package name 'hr'
    ],
    "core": [
        ("upload.py", "upload.py"),
        ("bulk_operations.py", "bulk.py"),
        ("analytics.py", "analytics.py")
    ]
}

# Move folders into core if needed (auth, users, admin_rbac)
core_folders = ["auth", "users", "admin_rbac"]
for folder in core_folders:
    src = os.path.join(base_dir, folder)
    dst = os.path.join(base_dir, "core", folder)
    if os.path.exists(src):
        try:
            shutil.move(src, dst)
            print(f"Moved {folder} to core/")
        except Exception as e:
            print(f"Error moving {folder}: {e}")


for folder, files in moves.items():
    target_dir = os.path.join(base_dir, folder)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    for src_file, dst_file in files:
        src = os.path.join(base_dir, src_file)
        dst = os.path.join(target_dir, dst_file)
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                print(f"Moved {src_file} to {folder}/{dst_file}")
            except Exception as e:
                print(f"Error moving {src_file}: {e}")
