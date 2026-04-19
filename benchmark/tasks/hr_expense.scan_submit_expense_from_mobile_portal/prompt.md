# Log a taxi ride from the My Expenses portal and submit it to manager

You are logged into Odoo 19 as **Administrator** and need to record a taxi
ride you took on a business trip, then push it to your manager for
approval.

## Steps

1. Open the **Expenses** app (the **My Expenses** view).
2. Click **New** to create a new expense.
3. Fill the new expense form with these **exact** values:
   - **Category / Product**: `Travel - Taxi`
   - **Description**: `Airport taxi`
   - **Total**: `45.00`
   - **Expense Date**: today's date (`2026-04-19`)
   - **Employee**: leave as the Administrator's employee record (auto-filled)
4. **Save** the expense.
5. Submit the expense to the manager via the expense workflow — in Odoo 19
   this means clicking the **Create Report** button on the saved expense's
   form status bar, which groups it into a report, then clicking **Submit
   to Manager** on the report so the expense moves out of the `draft`
   state. If the flow auto-creates the report, just click **Submit to
   Manager**.

The expense's `state` must end up as **Submitted / Reported / Approved**
(i.e., not still in `draft`).

## Rules

- The expense description must be exactly `Airport taxi` — no trailing
  punctuation, no different capitalization.
- The total must be exactly `45.00`.
- The product category on the expense must be exactly `Travel - Taxi`.
- Do not create multiple expenses — only the single `Airport taxi` one.
- Do not delete any other expense records.
- Do not reset the expense to draft after submitting.
