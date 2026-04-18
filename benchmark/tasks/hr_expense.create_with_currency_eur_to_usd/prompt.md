# Create a multi-currency expense (EUR) — converts to USD

You are in the Odoo 19 **Expenses** app logged in as **Administrator**.

The company currency is **USD**. You need to record an employee-paid expense
that was paid abroad in **Euros** so that the system converts the amount to USD
using the seeded exchange rate.

## What to do

1. In **Expenses**, click **New** to create a new expense.
2. Fill in the following fields:
   - **Description**: `NYC Hotel`
   - **Category**: `Hotel`
   - **Total**: `185.00`
   - **Currency** (the dropdown next to Total): change it from `USD` to **`EUR`**
   - **Expense Date**: `04/01/2026`
   - **Paid By**: keep **Employee (to reimburse)** (the default)
3. Save the expense (do **not** submit it). Leave it in **Draft** state.

After saving, the form should show the converted total in USD (the company
currency) underneath — this should read approximately **$200.00** at the
seeded rate.

## Rules

- The **Currency** must be **EUR**, not the default USD. This is the key step.
- **Total** must be `185.00` (in EUR).
- **Paid By** must remain **Employee (to reimburse)**.
- Use the seeded **Hotel** category exactly.
- Do **not** submit, post, approve, or refuse the expense.
- Do **not** modify any other expenses.
- Leave the record in **Draft** state.
