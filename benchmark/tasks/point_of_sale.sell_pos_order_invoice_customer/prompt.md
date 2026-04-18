Open the **Point of Sale** app and start the register **`Bench Invoice POS`** (accept the default opening cash of 0 if a control screen appears).

1. Add **`Bench Invoice Item`** to the cart with quantity **1**. The unit price is **€50.00**, so the order total must be **€50.00** (this product is tax-free — do not change the price).
2. Click the **Customer** button on the action pad and select the existing customer **`Invoice Iris`**. The customer name must now appear on the order header.
3. Click **Payment** to go to the payment screen.
4. On the payment screen, **enable the `Invoice` toggle** (the receipt-with-pencil icon, sometimes labelled "Invoice"). The toggle button must be in its active/highlighted state — the order must be marked as "to invoice" before you validate.
5. Choose the **`Bench Invoice Cash`** payment method, enter the full €50.00 (default tendered amount is fine), then click **Validate** to complete the sale.
6. After validation, the receipt screen should appear showing the order. Do **not** close the POS session.

When you finish, the POS order must be paid and an actual customer invoice (account.move) must have been generated and posted in Accounting for **Invoice Iris** for €50.00.

## Rules

- The `Invoice` toggle on the payment screen MUST be enabled before you click Validate. If you forget and just pay cash, the order will be paid but no invoice will be created — the task will fail.
- Use the customer **`Invoice Iris`** that is already seeded — do NOT create a new customer.
- Do not add any other product to the cart.
- Do not change the unit price of `Bench Invoice Item`.
- Do not refund or void the order after validation.
- Do not close the POS session.
