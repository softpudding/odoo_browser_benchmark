# Create a company-paid expense with vendor and notes

You are in the Odoo 19 **Expenses** app logged in as **Administrator**.

You need to record a company-paid expense (paid by the company credit card,
not reimbursable to the employee).

## What to do

1. In **Expenses**, click **New** to create a new expense.
2. Fill in the following:
   - **Description**: `Client dinner at Harborview`
   - **Category**: `Client Meals`
   - **Total**: `185.50`
   - **Expense Date**: `05/12/2026`
   - **Paid By**: select **Company** (not Employee)
   - **Vendor**: `Harborview Restaurant Group`
3. In the notes area, enter exactly:

   ```
   Q2 client retention dinner - VIP attendee list on file
   ```
4. Save the expense. Leave it in **Draft** state — do **not** submit it.

## Rules

- **Paid By** must be **Company** — do not leave it on Employee.
- Use the seeded **Harborview Restaurant Group** vendor exactly.
- Do **not** submit, post, or modify any other expenses.
- Leave the record in **Draft** state.
