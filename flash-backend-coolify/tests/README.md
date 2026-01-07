# Tests

## Overview
Test suite for the application.

## Structure
- `test_upload_db.py`: Tests for file upload and database persistence

## Running Tests
```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run specific test
pytest tests/test_upload_db.py
```

## Adding Tests
Follow the pattern in existing tests:
1. Import necessary fixtures
2. Create test functions with `test_` prefix
3. Use assertions to verify behavior
