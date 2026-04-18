# Refuse an expense report with a specific reason

You are in the Odoo 19 **Expenses** app logged in as **Administrator**
acting as the approver for the finance team.

An employee has submitted an expense report that must be **refused**
because the total on the attached receipt does not match the vendor
invoice on file.

## What to do

1. Go to the **Expenses** app and open the approver list of reports
   (the list that shows expenses waiting for approval).
2. Find the submitted expense named **INVOICE-MISMATCH-2026 — duplicate
   receipt** from employee **Jordan Whitfield**. The report is
   currently in the **Submitted** state.
3. Open the expense.
4. Click the **Refuse** button in the statusbar. A dialog appears
   asking for the refusal reason.
5. In that dialog, type exactly:

   `Receipt amount doesn't match invoice — please resubmit`

   Then confirm by clicking the **Refuse** / **Send** button in the
   dialog.
6. The expense should leave the **Submitted** state and move to
   **Refused**, and the reason you typed should appear in the chatter
   as a posted message.

## Rules

- Refuse **only** the INVOICE-MISMATCH-2026 expense; do not touch any
  other submitted expense.
- The refusal reason text must be the exact sentence above — do not
  confirm the dialog with an empty reason.
- Do **not** approve, post, or pay the expense.
- Do **not** delete the expense.
- Do **not** reset the expense to draft.
