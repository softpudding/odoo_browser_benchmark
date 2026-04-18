Confirmed sales order **S-BENCH-MS-001** for customer **Bench Milestone Client** has 1 line for the service product **Bench Milestone Service** (quantity 3). Confirming the order created a project with three milestones tied to that order line:

1. **Design Phase** — due 2026-05-01
2. **Build Phase** — due 2026-05-15
3. **Launch Phase** — due 2026-06-01

The customer has accepted the **Design Phase** deliverable only. Do all of the following:

1. Open the **Project** app, locate the project that was generated for `S-BENCH-MS-001`, and open its **Milestones** view.
2. Mark **only the "Design Phase" milestone as reached** (tick its **Reached** checkbox / set `is_reached` to true). Leave **Build Phase** and **Launch Phase** unreached.
3. Open the **Sales** app and open sales order **S-BENCH-MS-001**.
4. Click the **Create Invoice** button.
5. In the **Create invoices** wizard, keep **"Regular invoice"** selected (the default radio option) and click **Create Draft** (a.k.a. **Create Invoice**) to produce the draft invoice. The wizard should auto-populate quantity 1 because only one milestone has been reached.

End state to leave behind:

- Exactly 1 milestone on the project is reached and it is **Design Phase**. The other 2 milestones remain unreached.
- The order line on `S-BENCH-MS-001` shows delivered quantity = 1.
- Exactly 1 customer invoice (draft `account.move`) exists for **Bench Milestone Client**, with 1 invoice line for quantity **1** at unit price **1000.00** (subtotal 1000.00).

Rules:

- Do **not** mark Build Phase or Launch Phase as reached.
- Do **not** post / confirm / validate the invoice — leave it in **Draft** state.
- Do **not** select "Down payment (percentage)" or "Down payment (fixed amount)" in the wizard — keep the default **Regular invoice**.
- Do **not** modify the order lines, quantities, prices, or the customer.
