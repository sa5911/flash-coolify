# Models - Core

## Overview
Core system models for authentication, authorization, and file management.

## Models
- **User**: Application users with authentication credentials
- **Role**: User roles for RBAC
- **Permission**: Granular permissions for access control
- **File**: Metadata for uploaded files (local storage)

## Relationships
- User → Role (many-to-many via user_roles)
- Role → Permission (many-to-many via role_permissions)
- File → User (many-to-one, tracks uploader)
