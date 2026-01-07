import os
import shutil

base_dir = r"c:\Users\HomePC\Desktop\app\flash-backend-coolify\app\schemas"

dirs = ["client", "hr", "finance", "inventory", "fleet", "core"]
for d in dirs:
    path = os.path.join(base_dir, d)
    if not os.path.exists(path):
        os.makedirs(path)

# (SourceFile, TargetFolder)
moves = {
    "client": ["client_management.py"],
    "hr": [
        "attendance.py", "employee.py", "employee2.py", "employee_advance.py", 
        "employee_document.py", "employee_inactive.py", "employee_warning.py",
        "employee_warning_document.py", "leave_period.py", "payroll.py",
        "payroll_payment_status.py", "payroll_sheet_entry.py"
    ],
    "finance": ["expense.py", "finance.py"],
    "inventory": [
        "general_inventory.py", "restricted_inventory.py", 
        "inventory_assignment.py", "employee_inventory.py"
    ],
    "fleet": [
        "fuel_entry.py", "vehicle.py", "vehicle_assignment.py", 
        "vehicle_assignment_analytics.py", "vehicle_assignment_efficiency.py",
        "vehicle_document.py", "vehicle_image.py", "vehicle_maintenance.py"
    ],
    "core": ["rbac.py", "user.py"]
}

for folder, files in moves.items():
    target_dir = os.path.join(base_dir, folder)
    for file in files:
        src = os.path.join(base_dir, file)
        dst = os.path.join(target_dir, file)
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                print(f"Moved {file} to {folder}/")
            except Exception as e:
                print(f"Error moving {file}: {e}")
