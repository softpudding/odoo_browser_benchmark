# Create Balanced Manual Journal Entry

You must create a **new manual journal entry** (not an invoice) in the
Accounting app's **Miscellaneous Operations** journal, with three balanced
lines (one debit split across two credit revenue accounts), and post it.

## Steps

1. Open the **Accounting** app (top menu: `Accounting`).
2. In the main menu, go to **Accounting → Journal Entries**. This opens the
   Journal Entries list (NOT the Customer Invoices list).
3. Click **New** to create a new journal entry. The form is a plain journal
   entry form (no Customer field, no invoice-line tab — it has a **Journal
   Items** tab with Debit / Credit columns).
4. Fill the header:
   - **Reference**: `Bench Manual Adj 2026-04`
   - **Accounting Date**: `April 30, 2026` (04/30/2026)
   - **Journal**: `Miscellaneous Operations` (the general-type journal — leave
     the default if it is already set to Miscellaneous Operations)
5. In the **Journal Items** tab, add exactly **three** lines (total debit =
   total credit = 100.00):
   - Line 1: Account = `Bench Receivable`, **Partner** = `Bench Entity`,
     Label = `Manual adjustment receivable`, **Debit** = `100.00`,
     Credit = `0.00`
   - Line 2: Account = `Bench Sales Revenue`, Label = `Manual adjustment — sales`,
     Debit = `0.00`, **Credit** = `60.00`
   - Line 3: Account = `Bench Other Revenue`, Label = `Manual adjustment — other income`,
     Debit = `0.00`, **Credit** = `40.00`
6. **Save** the draft entry (the cloud/save icon). The three lines must
   balance (total debit = total credit = 100.00).
7. Click **Post** (in the header) to post the journal entry. After posting
   the header status should read **Posted**.

## Rules

- Create exactly **one** journal entry with **exactly three** journal-item
  lines.
- The entry's Accounting Date must be **2026-04-30** (not today's date).
- The entry must be in the **Miscellaneous Operations** journal (type
  `general`).
- Do **not** create any customer or vendor invoices — this is a direct
  journal entry (`move_type = entry`).
- The receivable line (Line 1) **must** have `Bench Entity` set as its
  Partner.
- Total debits must equal total credits: 100.00.
- Post the entry after saving — final state must be **Posted**.
