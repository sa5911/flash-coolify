import os
import re

# We effectively want to replace 'app.api.routes.hr.analytics_hr.<submodule>' with 'app.api.routes.hr.<submodule>'
# for the submodules that are actually in the hr package.

submodules = [
    "advances", "attendance", "documents", "employees2", "inactive", 
    "leave_periods", "payroll", "payroll2", "router", "warnings"
]

replacements = []
for sub in submodules:
    # Pattern: app.api.routes.hr.analytics_hr.submodule
    replacements.append((
        re.compile(rf'app\.api\.routes\.hr\.analytics_hr\.{sub}\b'),
        f'app.api.routes.hr.{sub}'
    ))

app_dir = r"c:\Users\HomePC\Desktop\app\flash-backend-coolify\app"

for root, dirs, files in os.walk(app_dir):
    for file in files:
        if not file.endswith('.py'):
            continue
            
        path = os.path.join(root, file)
        if 'scripts' in path: 
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
