# Models - Fleet

## Overview
Vehicle fleet management models.

## Models
- **Vehicle**: Vehicle registry (registration, model, status)
- **VehicleImage**: Photos of vehicles
- **FuelEntry**: Fuel transaction logs
- **VehicleMaintenance**: Repair and maintenance history
- **VehicleAssignment**: Driver/department assignments

## Relationships
- Vehicle → VehicleImage (one-to-many)
- Vehicle → FuelEntry (one-to-many)
- Vehicle → VehicleMaintenance (one-to-many)
- Vehicle → VehicleAssignment (one-to-many)
