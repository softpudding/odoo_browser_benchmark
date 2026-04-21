# Post an approved expense to its journal entry

You are in the Odoo 19 **Expenses** app logged in as **Administrator**
(an expense manager with accounting rights).

An approved employee expense is ready to be posted to the journal so
that the accounting entry is generated.

## What to do

1. Open the **Expenses** app.
2. Navigate to **Expenses > My Expenses** (the full expense list that
   shows every state).
3. Find the approved expense named **Bench Taxi Fare** by
   **Dana Silverstein** — it is currently in the **Approved** state
   with an amount of **42.50**.
4. Open the expense.
5. In the statusbar, click the **Post Journal Entries** button.
6. A **Post Expenses** dialog appears showing a Journal and an
   Accounting Date. Accept the prefilled defaults and click the
   **Post Expenses** button in the dialog footer to confirm.
7. After confirmation the expense must move to the **Posted** state,
   and a linked journal entry (account.move) is created.

## Rules

- Post **only** the Bench Taxi Fare expense.
- Do **not** refuse, reset, or delete the expense.
- Do **not** modify the amount, employee, date, or product of the
  expense.
- Do **not** change the journal or accounting date in the wizard —
  accept the defaults.
- Do **not** create any new expense.
