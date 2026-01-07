import os
import re

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

replacements = []
for folder, files in moves.items():
    for file in files:
        module = file.replace('.py', '')
        # Pattern 1: from app.models.module import ...
        # Replacement: from app.models.folder.module import ...
        replacements.append((
            re.compile(rf'from app\.models\.{module}\b'),
            f'from app.models.{folder}.{module}'
        ))
        # Pattern 2: import app.models.module
        replacements.append((
            re.compile(rf'import app\.models\.{module}\b'),
            f'import app.models.{folder}.{module}'
        ))

app_dir = r"c:\Users\HomePC\Desktop\app\flash-backend-coolify\app"

for root, dirs, files in os.walk(app_dir):
    for file in files:
        if not file.endswith('.py'):
            continue
            
        path = os.path.join(root, file)
        
        # Skip models/__init__.py as we manually fixed it, and skip this script if it's in app (it's not)
        if 'models' in path and '__init__.py' in path:
            continue
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for regex, replacement in replacements:
                new_content = regex.sub(replacement, new_content)
                
            if new_content != content:
                print(f"Fixing {path}")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        except Exception as e:
            print(f"Error processing {path}: {e}")
