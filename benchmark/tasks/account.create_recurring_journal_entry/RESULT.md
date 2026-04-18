ROW: 327
TASK_ID: account.create_recurring_journal_entry
DIFFICULTY: hard
SUMMARY: Create a balanced 3-line journal entry (move_type=entry) in Accounting -> Journal Entries for 2026-05-01, schedule a "To-Do" reminder activity for 2026-06-01, then Post the entry.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## account.create_recurring_journal_entry

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 213s first run, 288s second run) |
| **F1** | 1.0 |
| **Odoo modules** | Accounting (account) |
| **Workflow** | Navigate Accounting -> Journal Entries (NOT Customer Invoices). Click New. Fill Reference='Bench Rent Apr', Accounting Date=2026-05-01. On the Journal Items tab add three balanced lines: Rent debit 1000, Tax Paid debit 50, Bank credit 1050. Save. Open chatter Activities -> schedule To-Do "Post next month's rent entry" due 2026-06-01. Click Post. |
| **Capability tested** | Journal-entry form (different from invoice form: no Customer, Debit/Credit columns, line_ids tab); multi-line balance arithmetic; chatter activity scheduling; entry-specific Post button. |
| **Notes** | Calibrated hard but BU passed twice in a row (213s and 288s). The Journal Items tab is only visible if admin has `account.group_account_readonly`; the base snapshot admin has `group_system` which implies the accounting groups, but some runs saw the tab missing -- seed explicitly adds admin to `account.group_account_readonly`, `group_account_invoice`, and `group_account_user` to guarantee visibility. The `name` (Label) column uses `section_and_note_text` widget which renders a `<textarea>`, not `<input>` -- oracle had to target `input, textarea` for that cell. Account autocomplete shows "<code> <name>" pattern and substring matching (`has_text="Rent"`) wrongly matches "Current Assets" (contains "rent"); oracle does an exact-name match after splitting on whitespace. Per calibration guidance, added a 3rd line (Tax Paid 50) to push beyond the 2-line trivial pattern, but BU still solved; a further harden would require analytic distribution or per-line partner. |
