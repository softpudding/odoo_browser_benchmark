Confirmed sales order **S-BENCH-MS-002** for customer **Bench Quad Milestone Client** has 1 line for the service product **Bench Quad Milestone Service** (quantity 4). Confirming the order created a project with four milestones tied to that order line:

1. **M1 Setup** — already reached (`is_reached = True`)
2. **M2 Build** — already reached (`is_reached = True`)
3. **M3 Test** — not yet reached
4. **M4 Launch** — not yet reached

The customer has accepted **M1 Setup** and **M2 Build** only (these are already marked as Reached). The remaining two milestones (**M3 Test**, **M4 Launch**) are still in progress and **must stay unreached**. Do all of the following:

1. Open the **Sales** app and open sales order **S-BENCH-MS-002**.
2. Click the **Create Invoice** button at the top of the order.
3. In the **Create invoices** wizard, keep **"Regular invoice"** selected (the default radio option). The wizard will auto-detect that **2 of the 4 milestones** have been reached and pre-populate the line quantity to **2** (NOT 4). Verify the wizard quantity is 2, then click **Create Draft** (a.k.a. **Create Invoice**) to produce the draft invoice.

End state to leave behind:

- The two milestones **M1 Setup** and **M2 Build** remain reached. **M3 Test** and **M4 Launch** remain unreached.
- The order line on `S-BENCH-MS-002` shows delivered quantity = 2.
- Exactly 1 customer invoice (draft `account.move`) exists for **Bench Quad Milestone Client**, with 1 invoice line for quantity **2** at unit price **500.00** (subtotal 1000.00).

Rules:

- Do **not** mark M3 Test or M4 Launch as reached.
- Do **not** un-mark M1 Setup or M2 Build.
- Do **not** post / confirm / validate the invoice — leave it in **Draft** state.
- Do **not** select "Down payment (percentage)" or "Down payment (fixed amount)" in the wizard — keep the default **Regular invoice**.
- Do **not** override the auto-populated quantity to 4 (or any other value); accept the wizard default of 2.
- Do **not** modify the order lines, quantities, prices, or the customer.
