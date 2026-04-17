Create and approve an employee expense in Odoo Expenses.

1. Open the Expenses app.
2. Create a new expense for employee `Administrator`.
3. Use category `[HOTEL] Hotel Stay`.
4. Set the expense title to `Harbor Summit Hotel`.
5. Set the expense date to `04/08/2026`.
6. Set the total to `486.75`.
7. Upload the receipt file from `/tmp/hr_expense_submit_report_with_receipt_approve.svg`.
8. Save the expense.
9. Submit the expense.
10. Approve the expense.

Rules:
- Do not create more than one expense named `Harbor Summit Hotel`.
- Do not change the employee, title, date, or amount after approval.
- The expense must end in the `Approved` state and keep the uploaded receipt attached.
