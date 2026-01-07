# Models - Inventory

## Overview
Asset and inventory tracking models.

## Models
- **GeneralItem**: Standard inventory items (office supplies, equipment)
- **RestrictedItem**: Sensitive items requiring special tracking (security gear)
- **InventoryAssignment**: Tracking of item assignments to employees
- **StockMovement**: Stock in/out transactions

## Relationships
- GeneralItem → InventoryAssignment (one-to-many)
- RestrictedItem → InventoryAssignment (one-to-many)
- InventoryAssignment → Employee2 (many-to-one)

## Notes
Restricted items have additional approval workflows and stricter tracking requirements.
