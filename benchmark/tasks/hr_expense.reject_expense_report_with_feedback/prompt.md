# Refuse an expense with a written reason

You are in the Odoo 19 **Expenses** app logged in as **Administrator** in
the manager / approver role.

An employee has submitted an expense that must be **rejected** because
the claimed hotel rate exceeds the company's per-night cap.

## What to do

1. Go to **Expenses** (the manager / approver list) and find the
   submitted expense **SUMMIT-2026 — overpriced hotel night** from
   employee **Alice Benchmark**.
2. Open the expense. It is currently in the **Submitted** state.
3. Click **Refuse** (the statusbar button). A dialog appears asking
   for the refusal reason.
4. In the dialog, enter the reason: `Hotel rate exceeds company cap —
   please resubmit with itemised receipts under $200/night.` Then
   click **Refuse Expense** / **Send** to confirm.
5. The expense should move out of **Submitted** state to **Refused**
   and the reason should be posted in the chatter as a message.

## Rules

- Only refuse the **SUMMIT-2026** expense — do not approve or touch
  any other expense.
- The refusal reason text must be provided — do not click Refuse with an
  empty reason.
- Do **not** approve, post, or pay the report.
- Do **not** delete the report.
