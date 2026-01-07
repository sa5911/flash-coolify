import os
import re

# (Regex Pattern, Replacement String)
replacements = [
    (r'app\.api\.routes\.vehicles', 'app.api.routes.fleet'),
    (r'app\.api\.routes\.employees', 'app.api.routes.hr'),
    (r'app\.api\.routes\.client_management', 'app.api.routes.client'),
    
    # Files moved to core
    (r'app\.api\.routes\.auth', 'app.api.routes.core.auth'),
    (r'app\.api\.routes\.users', 'app.api.routes.core.users'),
    (r'app\.api\.routes\.admin_rbac', 'app.api.routes.core.admin_rbac'),
    (r'app\.api\.routes\.bulk_operations', 'app.api.routes.core.bulk'),
    (r'app\.api\.routes\.upload', 'app.api.routes.core.upload'),
    (r'app\.api\.routes\.analytics\b', 'app.api.routes.core.analytics'), # \b to avoid matching analytics_hr if it exists? No, hr.analytics_hr is different.
    
    # Files moved to fleet
    (r'app\.api\.routes\.fuel_entries', 'app.api.routes.fleet.fuel'),
    
    # Files moved to inventory
    (r'app\.api\.routes\.general_inventory', 'app.api.routes.inventory.general'),
    (r'app\.api\.routes\.restricted_inventory', 'app.api.routes.inventory.restricted'),
    (r'app\.api\.routes\.inventory_assignments', 'app.api.routes.inventory.assignments'),
    
    # Files moved to finance
    (r'app\.api\.routes\.expenses', 'app.api.routes.finance.expenses'),
    (r'app\.api\.routes\.exports_accounts', 'app.api.routes.finance.exports'),
    # Handle finance.py module -> finance.router module
    (r'app\.api\.routes\.finance\b', 'app.api.routes.finance.router'), 
    
    # HR file rename
    (r'app\.api\.routes\.hr\b', 'app.api.routes.hr.analytics_hr'),
]

app_dir = r"c:\Users\HomePC\Desktop\app\flash-backend-coolify\app"

for root, dirs, files in os.walk(app_dir):
    for file in files:
        if not file.endswith('.py'):
            continue
            
        path = os.path.join(root, file)
        
        # Skip this script and route_moves script
        if 'scripts' in path:
            continue
            
        # Skip app/api/routes/__init__.py because we manually fixed it and specific imports might be different
        if 'app\\api\\routes\\__init__.py' in path:
            continue
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for pattern, replacement in replacements:
                # Use sub with generated regex
                new_content = re.sub(pattern, replacement, new_content)
                
            if new_content != content:
                print(f"Fixing {path}")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        except Exception as e:
            print(f"Error processing {path}: {e}")
