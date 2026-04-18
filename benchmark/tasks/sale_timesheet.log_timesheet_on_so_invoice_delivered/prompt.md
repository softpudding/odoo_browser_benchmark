Confirmed sales order **S-BENCH-TS-001** for customer **Bench Services Co** has
1 line for the service product **Bench Consulting** (ordered quantity 10
hours, unit price 150.00). The product is invoiced **based on timesheets**,
so its delivered quantity is driven by hours logged on the task that
confirmation auto-generated.

The customer has already accepted 6 hours of work. Do all of the following:

1. Open the **Sales** app and open the sales order **S-BENCH-TS-001**.
2. Click the **Tasks** smart button (in the button box at the top of the
   order) to open the task that was auto-created when the order was
   confirmed. There is exactly **one task** for this order — open it.
3. On the task form, open the **Timesheets** tab and log **two**
   timesheet entries, both with **Administrator** as the **Employee**:
     - **First entry**: Date **2026-04-15**, Description **Initial
       consulting session**, **Time Spent 4:00** (4 hours).
     - **Second entry**: Date **2026-04-19** (today), Description
       **Follow-up session**, **Time Spent 2:00** (2 hours).
   Save the task so both timesheet rows persist.
4. Return to sales order **S-BENCH-TS-001** (breadcrumb or Sales app). On
   the order line for **Bench Consulting**, verify that **Delivered** now
   reads **6.00** (and ordered is still 10.00). If Delivered is still
   0.00, something went wrong — the timesheets did not persist.
5. Click the **Create Invoice** button on the order. In the **Create
   invoices** wizard, keep **"Regular invoice"** selected (the default
   radio at the top of the wizard — NOT "Down payment (percentage)" and
   NOT "Down payment (fixed amount)") and click **Create Draft** (a.k.a.
   **Create Invoice**). The wizard should auto-populate the invoice line
   at quantity **6.00** because that is the delivered amount.

End state to leave behind:

- The task for **S-BENCH-TS-001** has exactly **2 timesheet rows**,
  totalling **6.00 hours**, both with Administrator as the employee.
- The sale order line for **Bench Consulting** shows **qty_delivered =
  6.00**.
- Exactly **1 draft customer invoice** (`account.move` / `out_invoice`)
  exists for **Bench Services Co**, with a single product line for
  **Bench Consulting**, quantity **6.00** at unit price **150.00**
  (subtotal 900.00).

Rules:

- Do **not** modify the order lines, quantities, prices, or customer on
  the SO.
- Do **not** post / confirm / validate the invoice — leave it in
  **Draft** state.
- Do **not** select "Down payment (percentage)" or "Down payment (fixed
  amount)" in the wizard — keep the default **Regular invoice**.
- Do **not** cancel the SO.
- Do **not** add extra timesheet rows — exactly 2 entries totalling
  6.00 hours.
- The distractor product **Bench Widget Supply** (delivered-manual
  policy) is unrelated — do not touch it.
