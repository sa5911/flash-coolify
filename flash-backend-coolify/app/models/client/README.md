# Models - Client

## Overview
Database models for client management.

## Models
- **Client**: Customer/client profiles
- **ClientSite**: Service locations for clients
- **ClientContract**: Service agreements and billing terms
- **SiteGuardAllocation**: Assignment of security personnel to sites

## Relationships
- Client → ClientSite (one-to-many)
- Client → ClientContract (one-to-many)
- ClientSite → SiteGuardAllocation (one-to-many)
