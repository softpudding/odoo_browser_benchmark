# Scrap one defective screw consumed during production, then finish the MO

You are in the Odoo 19 **Manufacturing** app logged in as **Administrator**.

Manufacturing order **MO-BENCH-SCRAP** is a confirmed MO for **1** unit of
**Bench Assembly Kit**. Its Bill of Materials consumes **3 Bench Screw**
per kit.

While setting up the production run you notice that **one of the three
screws** on the Bench Screw component row is visibly **damaged**. Before
marking the order as done you must **scrap that one screw** so the scrap
shows up in Inventory reporting, and only **then** finish production.

## What to do

1. Open the **Manufacturing** app and go to **Operations → Manufacturing
   Orders**.
2. Open the manufacturing order **MO-BENCH-SCRAP**.
3. In the MO form, open the **cog / Actions** menu (the little vertical
   "3-dots" / gear icon next to the status bar) and click **Scrap**.
4. In the **Scrap Products** dialog that appears, fill in:
   - **Product**: `Bench Screw`
   - **Quantity**: `1`
   Leave the other fields (source location = `WH/Stock`, scrap location =
   the default virtual scrap location) at their default values.
5. Click **Scrap Products** (or **Validate**) in the dialog footer to
   validate the scrap.
6. You are returned to the MO form. Click **Produce All** (also labeled
   **Mark as Done**) in the form header.
7. If a confirmation or consumption-warning dialog appears, accept the
   defaults so the MO finishes with the 2 remaining screws consumed.

After you finish:

- Exactly **one** `stock.scrap` record should exist for MO
  **MO-BENCH-SCRAP**, with product **Bench Screw**, quantity **1**, and
  state **Done**.
- MO **MO-BENCH-SCRAP** should be in **Done** state with **1 unit
  produced**.

## Rules

- Do **not** cancel or unlock the manufacturing order.
- Do **not** change the planned quantity (1 unit of Bench Assembly Kit).
- Do **not** edit the Bill of Materials.
- Scrap **only Bench Screw**, quantity **1** — do **not** scrap a
  different product and do **not** scrap more than one unit.
- Do **not** create any additional manufacturing orders, unbuild orders,
  or extra scrap orders.
