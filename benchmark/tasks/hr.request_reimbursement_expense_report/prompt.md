# Submit, approve, and post an employee reimbursement expense

You are logged into Odoo 19 as **Administrator**. Your own `hr.employee` record
has a single pending reimbursement expense that needs to walk the full
Odoo 19 reimbursement lifecycle:

  **Draft → Submitted → Approved → Posted**

The seeded expense is:

| Field | Value |
|---|---|
| Description | `Bench Travel Expense` |
| Paid By | `Employee (to reimburse)` (`own_account`) |
| Total | `150.00` |
| Employee | the Administrator's `hr.employee` |
| State | `Draft` (not yet submitted) |

## Steps

1. Open the **Expenses** app. You should land on **My Expenses**.
2. Open the `Bench Travel Expense` expense (click its row — it is the draft
   line owned by the Administrator's employee).
3. On the expense form's statusbar, click **Submit**. The expense moves to
   the **Submitted** state and the manager is notified.
4. Still on the same form, click **Approve**. The expense moves to
   **Approved**. (You have both `Expense Team Approver` and `Expense
   Manager` groups, so the Approve button is available to you on your own
   expense.)
5. Click **Post Journal Entries**. A small dialog appears titled
   **Post Expenses** with two fields (Journal, Accounting Date) already
   pre-filled from defaults. Do **not** change those defaults. Just click
   the primary confirmation button **Post Expenses** in the dialog footer.
6. The expense lands in the **Posted** state and a corresponding
   `account.move` journal entry is created and posted. This is the Odoo 19
   equivalent of the legacy "Expense Report in Done state" from pre-Odoo
   19 — the `hr.expense.sheet` wrapper model no longer exists in v19,
   approvals now run directly on `hr.expense`.

## Rules

- Do **not** change the expense description, total, product, date, or
  employee. The seed already sets those — you only click through the
  state transitions.
- Do **not** reset the expense back to Draft once it has advanced.
- Do **not** refuse the expense.
- Do **not** create any new expenses or delete other expenses on the
  system.
- The Post Expenses wizard's two fields (Journal, Accounting Date) must
  be left at their defaults — don't edit them.
- The final state of the expense must be **Posted** (`state='posted'`).
  Leaving the expense in `Submitted` or `Approved` is not enough.
