# Refuse an expense report with a written reason

You are in the Odoo 19 **Expenses** app logged in as **Administrator** in
the manager / approver role.

An employee has submitted an expense report that must be **rejected**
because the claimed hotel rate exceeds the company's per-night cap.

## What to do

1. Go to **Expenses → Expense Reports → To Approve** (or the
   equivalent manager view) and find the submitted report
   **SUMMIT-2026 – Summit trip reimbursement** from employee
   **Alice Benchmark**.
2. Open the report. It is currently in the **Submitted** state.
3. Click **Refuse** (the statusbar button). A dialog appears asking
   for the refusal reason.
4. In the dialog, enter the reason: `Hotel rate exceeds company cap —
   please resubmit with itemised receipts under $200/night.` Then
   click **Refuse Expense** / **Send** to confirm.
5. The report should move out of **Submitted** state (typically to
   **Refused** / **Draft**) and the reason should be posted in the
   chatter as a message.

## Rules

- Only refuse the **SUMMIT-2026** report — do not approve or touch any
  other report.
- The refusal reason text must be provided — do not click Refuse with an
  empty reason.
- Do **not** approve, post, or pay the report.
- Do **not** delete the report.
