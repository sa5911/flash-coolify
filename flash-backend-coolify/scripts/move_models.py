import os
import shutil

moves = {
    "client": [
        "client.py", "client_address.py", "client_contact.py", "client_contract.py", 
        "client_document.py", "client_guard_requirement.py", "client_invoice.py", 
        "client_rate_card.py", "client_site.py", "client_site_guard_allocation.py"
    ],
    "hr": [
        "employee.py", "employee2.py", "employee_document.py", "employee_inactive.py", 
        "employee_warning.py", "employee_warning_document.py", "attendance.py", 
        "leave_period.py", "employee_advance.py", "employee_advance_deduction.py"
    ],
    "finance": [
        "finance_account.py", "finance_journal_entry.py", "finance_journal_line.py", 
        "expense.py", "payroll_payment_status.py", "payroll_sheet_entry.py"
    ],
    "inventory": [
        "general_item.py", "general_item_employee_balance.py", "general_item_transaction.py", 
        "restricted_item.py", "restricted_item_employee_balance.py", "restricted_item_image.py", 
        "restricted_item_serial_unit.py", "restricted_item_transaction.py", 
        "inventory_assignment.py"
    ],
    "fleet": [
        "vehicle.py", "vehicle_assignment.py", "vehicle_document.py", "vehicle_image.py", 
        "vehicle_maintenance.py", "fuel_entry.py"
    ],
    "core": [
        "user.py", "rbac.py"
    ]
}

base_dir = r"c:\Users\HomePC\Desktop\app\flash-backend-coolify\app\models"

for folder, files in moves.items():
    target_dir = os.path.join(base_dir, folder)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for file in files:
        src = os.path.join(base_dir, file)
        dst = os.path.join(target_dir, file)
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                print(f"Moved {file} to {folder}/")
            except Exception as e:
                print(f"Error moving {file}: {e}")
        else:
            print(f"Skipping {file} (not found)")
