# Scrap a defective component during production, then finish the MO

You are in the Odoo 19 **Manufacturing** app logged in as **Administrator**.

Manufacturing order **M-BENCH-SCRAP-001** is a confirmed MO for **5** units
of **Bench Widget**. Its Bill of Materials consumes **5 ScrewA** and
**5 ScrewB** per production run.

Before finishing production you need to **scrap 2 ScrewA units** because
they came from a defective batch, and only **then** produce the whole
order.

## What to do

1. Open the **Manufacturing** app and go to **Operations → Manufacturing
   Orders**.
2. Open the manufacturing order **M-BENCH-SCRAP-001**.
3. Open the form's **cog "Actions"** menu (the gear/settings icon next to
   the breadcrumb) and click **Scrap**.
4. In the **Scrap Products** dialog that opens, fill in:
   - **Product**: `ScrewA`
   - **Quantity**: `2`
   - **Scrap Reason**: add the existing tag `Defective batch`
   - **Source Location**: `WH/Stock` (i.e., the main warehouse stock
     location — **not** the scrap / virtual location)
   Leave the **Scrap Location** at its default (the company's scrap /
   virtual inventory location).
5. Click **Scrap Products** in the dialog footer to validate the scrap.
6. You are returned to the MO form. Click **Produce All** (also labeled
   "Mark as Done") in the form header.
7. If any confirmation or consumption-warning dialog appears, accept the
   defaults (keep the already-consumed components, confirm the full
   production of 5 units).

After you finish:

- Exactly **one** `stock.scrap` record should exist for MO
  M-BENCH-SCRAP-001, with product **ScrewA**, quantity **2**, reason tag
  **Defective batch**, and state **Done**.
- MO **M-BENCH-SCRAP-001** should be in **Done** state with
  **5 units produced**.

## Rules

- Do **not** cancel or unlock the manufacturing order.
- Do **not** change the planned quantity (5 units of Bench Widget).
- Do **not** modify the Bill of Materials or the component lines.
- Scrap **only ScrewA**, quantity **2** — do **not** scrap ScrewB, and do
  not create multiple scrap records.
- The scrap reason tag must be **Defective batch** (the tag already
  exists — select it from the dropdown, do not create a new one).
- Do **not** create any additional manufacturing orders, unbuild orders,
  or scrap orders.
