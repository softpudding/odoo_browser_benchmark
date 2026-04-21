# Split a draft expense 50/50 across two analytic accounts

You are in the Odoo 19 **Expenses** app logged in as **Administrator**.

A draft travel expense needs its cost split evenly between two analytic
projects before it is submitted for approval.

## What to do

1. Open the **Expenses** app.
2. Navigate to **Expenses > My Expenses** (the full list that
   includes every state and owner) so the draft expense is visible.
3. Find and open the draft expense **Bench Split Travel** for
   **Morgan Pearce** — it is currently **Draft** with a total amount
   of **200.00**.
4. In the expense form, locate the **Analytic Distribution** field
   (in the main form, not in Journal Items).
5. Open the analytic distribution editor and set **exactly two**
   lines:
   - **Bench Project Alpha** — **50%**
   - **Bench Project Beta** — **50%**
   The two percentages must sum to 100%. Remove any other rows that
   may appear.
6. Close the analytic distribution editor so the field is saved onto
   the expense.
7. Save the expense form if it is still dirty.
8. Click the **Submit** button on the statusbar so the
   expense moves out of Draft into the submitted state.

## Rules

- Use **only** Bench Project Alpha (50%) and Bench Project Beta
  (50%) — do not pick any other analytic account.
- Do **not** change the expense name, employee, product, amount, or
  date.
- Do **not** refuse, approve, post, or delete the expense.
- Do **not** create additional expenses or analytic accounts.
- The final state of the expense must be **submitted** (not draft).
