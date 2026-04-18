# Create Recurring Rent Journal Entry

You must create a **new journal entry** (not an invoice) in the Accounting app for the monthly rent accrual, and schedule a follow-up activity to remind you to post next month's entry.

## Steps

1. Open the **Accounting** app (top menu: `Accounting`).
2. In the main menu, go to **Accounting → Journal Entries**. This opens the Journal Entries list (NOT the Customer Invoices list).
3. Click **New** to create a new journal entry. The form is a plain journal entry form (no Customer field, no invoice-line tab — it has a **Journal Items** tab with Debit / Credit columns).
4. Fill the header:
   - **Reference**: `Bench Rent Apr`
   - **Accounting Date**: `May 1, 2026` (05/01/2026)
   - **Journal**: `Miscellaneous Operations` (leave the default if it is already set to Miscellaneous)
5. In the **Journal Items** tab, add exactly **three** lines (the entry must balance: total debits = total credits = 1050.00):
   - Line 1: Account = `Rent`, Label = `April rent expense`, **Debit** = `1000.00`, Credit = `0.00`
   - Line 2: Account = `Tax Paid`, Label = `Input tax on rent`, **Debit** = `50.00`, Credit = `0.00`
   - Line 3: Account = `Bank`, Label = `April rent payment`, Debit = `0.00`, **Credit** = `1050.00`
6. **Save** the draft entry (the cloud/save icon). The three lines must balance (total debit = total credit = 1050.00).
7. Now schedule a reminder activity on this entry. In the chatter (below the form) click **Activities** and schedule an activity:
   - **Activity Type**: `To-Do`
   - **Summary**: `Post next month's rent entry`
   - **Due Date**: `June 1, 2026` (06/01/2026)
   - Click **Schedule** to save the activity.
8. Back on the entry form, click **Post** (in the header) to post the journal entry. After posting the header status should read **Posted**.

## Rules

- Create exactly **one** journal entry with **exactly three** journal-item lines.
- The entry's Accounting Date must be **2026-05-01** (not today's date).
- Do **not** create any customer or vendor invoices — this is a direct journal entry (`move_type = entry`).
- The activity summary must contain "Post next month's rent entry" (so the check can match it).
- Post the entry after saving and scheduling the activity — final state must be **Posted**.
