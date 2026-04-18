# Save Draft Journal Entry as a Monthly Recurring Template

A draft journal entry has already been prepared for recurring office-supply accruals. Your job is to **convert this existing draft entry into a monthly recurring template** so that Odoo auto-posts a copy for each of the next three months.

## Seeded state

The following **draft** journal entry already exists in **Accounting -> Journal Entries** (it is NOT a customer/vendor invoice):

- **Reference**: `Bench Office Supplies Tmpl`
- **Accounting Date**: `May 1, 2026` (05/01/2026)
- **Journal**: `Miscellaneous Operations`
- **Status**: `Draft`
- Two balanced Journal Items totalling $500.00 (Debit = Credit = 500.00):
  - `Office Supplies` debit 500.00
  - `Bank` credit 500.00

Do **not** change any of these lines, the reference, the accounting date, or the journal. Do **not** post the entry.

## Steps

1. Open the **Accounting** app.
2. In the menu go to **Accounting -> Journal Entries** (NOT Customer Invoices).
3. Open the draft entry with Reference **`Bench Office Supplies Tmpl`** (its status should read **Draft**).
4. Click the **Other Info** tab in the notebook at the bottom of the form.
5. Change the **Auto-post** field from `No` to **`Monthly`**. A new field **Auto-post until** will appear once Monthly is selected.
6. Set **Auto-post until** to **`August 1, 2026`** (08/01/2026). This stops the recurrence after three monthly copies (May, June, July).
7. **Save** the form (the cloud icon or Save button). The entry must remain in **Draft** state.

## Rules

- Do **not** create a new journal entry — edit the existing draft.
- Do **not** post the entry — the final state must still be **Draft**.
- Do **not** modify the Reference, Accounting Date, Journal, or any journal-item lines.
- The Auto-post selection must end up as **Monthly** (exact label).
- The Auto-post until date must be exactly **2026-08-01**.
