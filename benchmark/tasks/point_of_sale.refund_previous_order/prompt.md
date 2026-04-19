Go to the **Point of Sale** app and open the register **`Bench Refund POS`** (the session is already open; accept the default opening cash of 0 if prompted).

A prior paid order already exists in this session:

- Reference: **`BENCH-REFUND-01`** (name: **`Bench Refund POS - 000001`**)
- One line: **`Bench Widget`** x **3** at **€10.00** each — total **€30.00**, paid in cash

The customer is returning **1** Bench Widget (keeping the other 2). Partially refund that one unit.

1. From the POS cart screen, open the **Orders** list (the **Orders** / ticket-screen button on the POS top bar, or the **"Review Orders"** button).
2. Locate the order **`Bench Refund POS - 000001`** (reference **`BENCH-REFUND-01`**) in the list and open it.
3. Click the **Refund** button on that order. Odoo opens a new refund cart pre-filled with the full line.
4. On the refund screen, select the **`Bench Widget`** line and **change the refund quantity to `1`** (the numpad **Qty** key, then **1**) so only **1** unit is refunded, not 3. The refund line should read **Bench Widget** at qty **1** for a refund subtotal of **€10.00** (shown as -€10.00 on the order).
5. Click **Payment**, choose the **`Bench Refund Cash`** payment method, and validate the payment. The refund amount is **-€10.00** (€10 cash back to the customer).

When done, the refund order must be in the **paid** state with `is_refund=True`, exactly one line (`Bench Widget`, qty -1, price_unit 10.00), amount_total -10.00, and a single -€10.00 cash payment on the seeded **`Bench Refund Cash`** method.

## Rules

- Do NOT refund more than 1 Bench Widget (the default refund is 3 — you must reduce it).
- Do NOT change the unit price (must stay at €10.00).
- Do NOT cancel or edit the original **`Bench Refund POS - 000001`** order.
- Do NOT add any other product to the refund cart.
- Do NOT close the POS session after the refund.
- Do NOT apply any discount on the refund line.
- Use the **`Bench Refund Cash`** payment method (not any other method).
