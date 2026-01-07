# Frontend Application Structure (Schema)

This document outlines the structure and schema of the **Flash ERP Frontend** application built with **Next.js 15 (App Router)**.

## 1. Technical Stack
- **Framework**: Next.js 15 (App Router)
- **UI Library**: Ant Design (v5/v6)
- **Styling**: Tailwind CSS + CSS Modules
- **State Management**: React Hooks + URL State
- **Icons**: Ant Design Icons

## 2. Directory Structure Overview
```
src/
├── app/                 # App Router (Pages & Layouts)
│   ├── (dashboard)/     # Protected Dashboard Routes (Wrapped in Shell)
│   ├── login/           # Login Page
│   ├── api/             # Next.js API Routes (Proxy)
│   ├── layout.tsx       # Root Layout
│   └── globals.css      # Global Styles (Tailwind)
├── components/          # Shared UI Components
│   └── DashboardShell   # Main Sidebar/Header Wrapper
└── lib/                 # Utilities (API clients, formatting)
```

## 3. Route Schema (Pages)
The application is organized into modules within the `(dashboard)` group.

| Route (URL) | Module | Description |
|---|---|---|
| `/dashboard` | **Overview** | Main stats and KPI dashboard |
| `/employees` | **HR** | Employee list, search, and management |
| `/employees2` | **HR** | Enhanced employee management (v2) |
| `/employees-inactive` | **HR** | Archive of inactive employees |
| `/attendance` | **HR** | Daily attendance tracking and reports |
| `/payroll` | **HR** | Payroll processing and salary slips |
| `/payroll2` | **HR** | Enhanced payroll system |
| `/client-management` | **CRM** | Client contracts, sites, and billing |
| `/accounts-advances` | **Finance** | Employee advances and loan management |
| `/finance` | **Finance** | General ledger, expenses, and accounts |
| `/vehicles` | **Fleet** | Vehicle registry and details |
| `/vehicle-assignments` | **Fleet** | Vehicle allocation to routes/drivers |
| `/vehicle-maintenance` | **Fleet** | Maintenance logs and scheduling |
| `/fuel-mileage` | **Fleet** | Fuel consumption tracking |
| `/general-inventory` | **Inventory** | General items (consumables, etc.) |
| `/restricted-inventory` | **Inventory** | Sensitive/Restricted items (weapons, etc.) |
| `/performance` | **Analytics** | Performance metrics and charts |
| `/super-admin` | **Admin** | User management and system settings |

## 4. Key Components

### `DashboardShell.tsx`
*   **Location**: `src/components/DashboardShell.tsx`
*   **Purpose**: The main wrapper for all dashboard pages.
*   **Features**:
    *   Sidebar Navigation (Responsive)
    *   Top Header (User profile, Notifications)
    *   Breadcrumbs

### `NotificationDropdown.tsx`
*   **Location**: `src/components/NotificationDropdown.tsx`
*   **Purpose**: Displays system notifications in the header.

## 5. API Integration Pattern
*   **Proxy**: The frontend uses a Next.js API Rewrite (`next.config.js`) to forward requests to the Backend.
*   **Frontend Call**: `GET /api/employees`
*   **Rewrites To**: `GET http://127.0.0.1:8000/api/v1/employees`
*   **Authentication**: JWT Tokens are stored in cookies/local storage used by the HTTP client.

## 6. Access Control (RBAC)
Refer to the `super-admin` module for Role-Based Access Control configuration.
- **Roles**: SuperAdmin, EmployeeEntry, AttendanceManager, etc.
- **Permissions**: Defined in the backend and potentially checked in `DashboardShell` or individual pages.
