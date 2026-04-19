# Post Opening Balance Journal Entry (Initial Equity)

The company is opening its books and needs an **opening balance journal entry** posted in the Miscellaneous Operations journal. You must create this entry **from scratch** as a plain journal entry (not an invoice), with two balanced lines, and post it.

## Steps

1. Open the **Accounting** app (top menu: `Accounting`).
2. In the main menu, go to **Accounting → Journal Entries**. This opens the Journal Entries list (NOT the Customer Invoices list).
3. Click **New** to create a new journal entry. The form is a plain journal entry form (no Customer field, no invoice-line tab — it has a **Journal Items** tab with Debit / Credit columns).
4. Fill the header:
   - **Reference**: `OPEN-BAL-001`
   - **Accounting Date**: `January 1, 2026` (01/01/2026)
   - **Journal**: `Miscellaneous Operations` (leave the default if it is already set to Miscellaneous)
5. In the **Journal Items** tab, add exactly **two** lines (the entry must balance: total debits = total credits = 10000.00):
   - Line 1: Account = `Stock Valuation` (code `140000`), Label = `Opening stock valuation`, **Debit** = `10000.00`, Credit = `0.00`
   - Line 2: Account = `Opening Balance`, Label = `Initial equity contribution`, Debit = `0.00`, **Credit** = `10000.00`
6. **Save** the draft entry (the cloud/save icon). The two lines must balance (total debit = total credit = 10000.00).
7. Click **Post** (in the header) to post the journal entry. After posting the header status should read **Posted**.

## Rules

- Create exactly **one** journal entry with **exactly two** journal-item lines.
- The entry's Accounting Date must be **2026-01-01** (not today's date).
- The entry's Reference must be exactly `OPEN-BAL-001`.
- Do **not** create any customer or vendor invoices — this is a direct journal entry (`move_type = entry`).
- The debit account must be `Stock Valuation` (an asset account, code `140000`).
- The credit account must be `Opening Balance` (an equity account).
- Post the entry after saving — final state must be **Posted** with `amount_total_signed = 0` (balanced).
- Do NOT click Reverse Entry or reset to draft; leave the posted entry in place.
