import sys
import os

sys.path.insert(0, os.getcwd())

try:
    print("Attempting to import app.api.routes.hr")
    import app.api.routes.hr
    print("Success: import app.api.routes.hr")
except Exception as e:
    print(f"Failed: import app.api.routes.hr: {e}")

try:
    print("Attempting to import app.api.routes.hr.analytics_hr")
    import app.api.routes.hr.analytics_hr
    print("Success: import app.api.routes.hr.analytics_hr")
except Exception as e:
    print(f"Failed: import app.api.routes.hr.analytics_hr: {e}")

try:
    print("Attempting to import app.api.routes")
    import app.api.routes
    print("Success: import app.api.routes")
except Exception as e:
    print(f"Failed: import app.api.routes: {e}")
