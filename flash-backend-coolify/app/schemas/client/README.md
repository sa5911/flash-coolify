# Schemas - Client

## Overview
Pydantic schemas for client API request/response validation.

## Schemas
- **ClientBase**: Base client fields
- **ClientCreate**: Client creation payload
- **ClientUpdate**: Client update payload
- **Client**: Full client response (with ID)
- **ClientSite**, **ClientContract**: Similar patterns for related entities

## Usage
Used in FastAPI route definitions for automatic validation and OpenAPI documentation.
