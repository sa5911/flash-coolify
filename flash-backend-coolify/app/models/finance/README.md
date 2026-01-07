# Models - Finance

## Overview
Financial transaction and accounting models.

## Models
- **Expense**: Operational expense records
- **FinanceAccount**: Chart of accounts
- **FinanceJournalEntry**: General ledger entries (double-entry bookkeeping)
- **PayrollSheetEntry**: Monthly payroll calculations
- **PayrollPaymentStatus**: Payment tracking for salaries

## Relationships
- FinanceJournalEntry → FinanceAccount (many-to-one for debit/credit accounts)
- PayrollSheetEntry → Employee2 (many-to-one)
