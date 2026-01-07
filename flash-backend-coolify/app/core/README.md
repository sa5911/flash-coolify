# Core Module

## Overview
Core application infrastructure including configuration, database, security, and utilities.

## Components
- **config.py**: Application settings and environment variables
- **database.py**: SQLAlchemy database connection and session management
- **security.py**: Password hashing and JWT token utilities
- **upload_helper.py**: File upload utilities (local storage)
- **startup_tasks.py**: Application initialization and seeding

## Usage
This module is imported by all other modules for shared infrastructure.
