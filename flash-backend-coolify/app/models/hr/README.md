# Models - HR

## Overview
Human resources and payroll models.

## Models
- **Employee2**: Main employee records (profiles, documents, bank details)
- **EmployeeInactive**: Archive for terminated employees
- **AttendanceRecord**: Daily attendance logs
- **LeaveRequest**: Leave applications
- **PayrollSheetEntry**: Monthly salary calculations (in finance module)

## Relationships
- Employee2 → AttendanceRecord (one-to-many)
- Employee2 → LeaveRequest (one-to-many)
- Employee2 → PayrollSheetEntry (one-to-many)

## Notes
Employee2 is the active employee table. When employees are terminated, they are moved to EmployeeInactive.
