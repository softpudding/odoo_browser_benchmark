# Scrap a defective component in an in-progress MO, then finish it

You are in the Odoo 19 **Manufacturing** app logged in as **Administrator**.

Manufacturing order **M-BENCH-PROD-001** is already **in progress** for
**5** units of **Bench Final Product**. Its Bill of Materials consumes
**5 Bench Component A** and **5 Bench Component B** per production run,
and the components are already reserved and being produced.

During the run, the operator noticed that **2 units of Bench Component A**
were damaged. You must **scrap exactly 2 units of Bench Component A**
through the MO's **Scrap** action, and **then finish the manufacturing
order**.

## What to do

1. Open the **Manufacturing** app and go to **Operations → Manufacturing
   Orders**.
2. Open the manufacturing order **M-BENCH-PROD-001**.
3. Open the form's **cog "Actions"** menu (the gear/settings icon next to
   the breadcrumb) and click **Scrap**.
4. In the **Scrap Products** dialog that opens, fill in:
   - **Product**: `Bench Component A` (the one with letter A — NOT
     Bench Component B)
   - **Quantity**: `2`
   Leave the other fields at their defaults (source location WH/Stock,
   destination the company scrap location).
5. Click **Scrap Products** (or **Validate**) in the dialog footer so
   the scrap moves to state **Done**.
6. You are returned to the MO form. Click **Produce All** (also labeled
   "Mark as Done") in the form header.
7. If any confirmation or consumption-warning dialog appears, accept the
   defaults so the MO transitions to **Done** with the full 5 units
   produced.

After you finish:

- Exactly **one** `stock.scrap` record should exist for MO
  M-BENCH-PROD-001, with product **Bench Component A**, quantity **2**,
  and state **Done**.
- MO **M-BENCH-PROD-001** should be in **Done** state with **5 units
  produced**.

## Rules

- Do **not** cancel or unlock the manufacturing order.
- Do **not** change the planned quantity (5 units of Bench Final
  Product).
- Do **not** modify the Bill of Materials or the component lines.
- Scrap **only Bench Component A**, quantity **2** — do **not** scrap
  Bench Component B, and do not create multiple scrap records.
- Do **not** create any additional manufacturing orders, unbuild
  orders, or scrap orders.
