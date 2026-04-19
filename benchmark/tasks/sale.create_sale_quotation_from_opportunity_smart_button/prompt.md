# Create a quotation from the opportunity's Quotations smart button

You are in the Odoo 19 **CRM** app logged in as **Administrator**.

The opportunity **Bench Opp Sale** (customer **Bench Opp Co**) needs a
draft quotation generated **through its own Quotations smart button** so
the new sale order is automatically linked back to the opportunity.

## What to do

1. Open the **CRM** app's pipeline (Kanban).
2. Find the opportunity **Bench Opp Sale** and open its form.
3. In the opportunity form, click the **Quotations** smart button
   (the button in the button box near the top of the form that shows a
   count of Quotations). This is the button whose internal field is
   `quotation_count`.
4. You will land on a **Quotations list** filtered to this opportunity
   (it will be empty). Click **New** to create a new quotation.
5. On the sale.order form that opens:
   - The **Customer** should already be **Bench Opp Co** (leave it).
   - Click **Add a product** on the Order Lines tab and pick
     **Bench Opp Product**.
   - Set the **Quantity** on that line to **2** (unit price stays at
     **100.00**).
6. **Save** the quotation (do **not** click **Confirm**). It must stay
   in the **Quotation** (draft) state.

After the task:
- A new `sale.order` exists with **Customer = Bench Opp Co**.
- The new order is linked to the opportunity **Bench Opp Sale**
  (internal field `opportunity_id`).
- The order has exactly **one** line: **Bench Opp Product**, qty **2**,
  unit price **100.00**.
- The order is a **Quotation** (state `draft`) — not confirmed.

## Rules

- You **must** create the quotation by clicking the **Quotations** smart
  button on the opportunity and then **New** — do **not** use the header
  **New Quotation** button, and do **not** create the quotation straight
  from the **Sales** app (that would leave `opportunity_id` empty and
  fail the check).
- Do **not** change the customer (must stay **Bench Opp Co**).
- Do **not** change the unit price on the product line (leave **100.00**).
- Do **not** click **Confirm** / **Send by Email** — the order must
  remain a **draft** Quotation.
- Do **not** create any additional sale.orders or opportunities.
