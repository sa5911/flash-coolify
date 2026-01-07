import os
import re

# (Regex Pattern, Replacement String)
replacements = [
    # Core
    (r'app\.schemas\.user\b', 'app.schemas.core.user'),
    (r'app\.schemas\.rbac\b', 'app.schemas.core.rbac'),
    
    # Fleet
    (r'app\.schemas\.vehicle\b', 'app.schemas.fleet.vehicle'),
    (r'app\.schemas\.vehicle_image\b', 'app.schemas.fleet.vehicle_image'),
    (r'app\.schemas\.vehicle_document\b', 'app.schemas.fleet.vehicle_document'),
    (r'app\.schemas\.fuel_entry\b', 'app.schemas.fleet.fuel_entry'),
    (r'app\.schemas\.vehicle_assignment\b', 'app.schemas.fleet.vehicle_assignment'),
    (r'app\.schemas\.vehicle_assignment_analytics\b', 'app.schemas.fleet.vehicle_assignment_analytics'),
    (r'app\.schemas\.vehicle_assignment_efficiency\b', 'app.schemas.fleet.vehicle_assignment_efficiency'),
    (r'app\.schemas\.vehicle_maintenance\b', 'app.schemas.fleet.vehicle_maintenance'),
    
    # HR
    (r'app\.schemas\.employee\b', 'app.schemas.hr.employee'),
    (r'app\.schemas\.employee2\b', 'app.schemas.hr.employee2'),
    (r'app\.schemas\.attendance\b', 'app.schemas.hr.attendance'),
    (r'app\.schemas\.leave_period\b', 'app.schemas.hr.leave_period'),
    (r'app\.schemas\.employee_document\b', 'app.schemas.hr.employee_document'),
    (r'app\.schemas\.employee_warning\b', 'app.schemas.hr.employee_warning'),
    (r'app\.schemas\.employee_warning_document\b', 'app.schemas.hr.employee_warning_document'),
    (r'app\.schemas\.payroll\b', 'app.schemas.hr.payroll'),
    (r'app\.schemas\.payroll_payment_status\b', 'app.schemas.hr.payroll_payment_status'),
    (r'app\.schemas\.payroll_sheet_entry\b', 'app.schemas.hr.payroll_sheet_entry'),
    (r'app\.schemas\.employee_advance\b', 'app.schemas.hr.employee_advance'),
    (r'app\.schemas\.employee_inactive\b', 'app.schemas.hr.employee_inactive'),

    # Finance
    (r'app\.schemas\.finance\b', 'app.schemas.finance.finance'),
    (r'app\.schemas\.expense\b', 'app.schemas.finance.expense'),
    
    # Inventory
    (r'app\.schemas\.inventory_assignment\b', 'app.schemas.inventory.inventory_assignment'),
    (r'app\.schemas\.general_inventory\b', 'app.schemas.inventory.general_inventory'),
    (r'app\.schemas\.restricted_inventory\b', 'app.schemas.inventory.restricted_inventory'),
    (r'app\.schemas\.employee_inventory\b', 'app.schemas.inventory.employee_inventory'),

    # Client
    (r'app\.schemas\.client_management\b', 'app.schemas.client.client_management'),
]

app_dir = r"c:\Users\HomePC\Desktop\app\flash-backend-coolify\app"

for root, dirs, files in os.walk(app_dir):
    for file in files:
        if not file.endswith('.py'):
            continue
            
        path = os.path.join(root, file)
        
        # Skip this script
        if 'scripts' in path:
            continue
            
        # Skip app/schemas/__init__.py as we manually updated it
        if 'app\\schemas\\__init__.py' in path:
            continue

        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for pattern, replacement in replacements:
                new_content = re.sub(pattern, replacement, new_content)
                
            if new_content != content:
                print(f"Fixing {path}")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        except Exception as e:
            print(f"Error processing {path}: {e}")
