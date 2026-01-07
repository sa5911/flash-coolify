"""Models package initialization."""

from app.models.core.user import User
from app.models.fleet.vehicle import Vehicle
from app.models.fleet.vehicle_document import VehicleDocument
from app.models.fleet.vehicle_assignment import VehicleAssignment
from app.models.hr.employee_document import EmployeeDocument
from app.models.hr.employee_warning import EmployeeWarning
from app.models.hr.employee_warning_document import EmployeeWarningDocument
from app.models.fleet.vehicle_image import VehicleImage
from app.models.fleet.fuel_entry import FuelEntry
from app.models.hr.employee import Employee
from app.models.fleet.vehicle_maintenance import VehicleMaintenance
from app.models.finance.payroll_payment_status import PayrollPaymentStatus
from app.models.hr.employee_advance import EmployeeAdvance
from app.models.hr.employee_advance_deduction import EmployeeAdvanceDeduction
from app.models.finance.payroll_sheet_entry import PayrollSheetEntry
from app.models.finance.expense import Expense
from app.models.hr.attendance import AttendanceRecord
from app.models.client.client import Client
from app.models.client.client_address import ClientAddress
from app.models.client.client_contact import ClientContact
from app.models.client.client_contract import ClientContract
from app.models.client.client_document import ClientDocument
from app.models.client.client_guard_requirement import ClientGuardRequirement
from app.models.client.client_invoice import ClientInvoice
from app.models.client.client_rate_card import ClientRateCard
from app.models.client.client_site import ClientSite
from app.models.client.client_site_guard_allocation import ClientSiteGuardAllocation
from app.models.hr.employee2 import Employee2
from app.models.hr.employee_inactive import EmployeeInactive
from app.models.finance.finance_account import FinanceAccount
from app.models.finance.finance_journal_entry import FinanceJournalEntry
from app.models.finance.finance_journal_line import FinanceJournalLine
from app.models.inventory.general_item import GeneralItem
from app.models.inventory.general_item_employee_balance import GeneralItemEmployeeBalance
from app.models.inventory.general_item_transaction import GeneralItemTransaction
from app.models.inventory.inventory_assignment import InventoryAssignmentState
from app.models.hr.leave_period import LeavePeriod
from app.models.core.rbac import Role, Permission
from app.models.inventory.restricted_item import RestrictedItem
from app.models.inventory.restricted_item_employee_balance import RestrictedItemEmployeeBalance
from app.models.inventory.restricted_item_image import RestrictedItemImage
from app.models.inventory.restricted_item_serial_unit import RestrictedItemSerialUnit
from app.models.inventory.restricted_item_transaction import RestrictedItemTransaction

__all__ = [
    "User",
    "Vehicle",
    "VehicleDocument",
    "EmployeeDocument",
    "EmployeeWarning",
    "EmployeeWarningDocument",
    "VehicleImage",
    "FuelEntry",
    "Employee",
    "VehicleMaintenance",
    "PayrollPaymentStatus",
    "EmployeeAdvance",
    "EmployeeAdvanceDeduction",
    "PayrollSheetEntry",
    "Expense",
    "AttendanceRecord",
    "Client",
    "ClientAddress",
    "ClientContact",
    "ClientContract",
    "ClientDocument",
    "ClientGuardRequirement",
    "ClientInvoice",
    "ClientRateCard",
    "ClientSite",
    "ClientSiteGuardAllocation",
    "Employee2",
    "EmployeeInactive",
    "FinanceAccount",
    "FinanceJournalEntry",
    "FinanceJournalLine",
    "GeneralItem",
    "GeneralItemEmployeeBalance",
    "GeneralItemTransaction",
    "InventoryAssignmentState",
    "LeavePeriod",
    "Role",
    "Permission",
    "RestrictedItem",
    "RestrictedItemEmployeeBalance",
    "RestrictedItemImage",
    "RestrictedItemSerialUnit",
    "RestrictedItemTransaction",
]
