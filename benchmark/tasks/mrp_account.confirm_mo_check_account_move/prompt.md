You are in the Odoo 19 **Manufacturing** app as **Administrator**.
A confirmed manufacturing order **M-BENCH-ACC-001** for **5 units** of
**Bench Manuf Item** is already seeded. The finished product uses
**automated (real-time) stock valuation**, so closing this MO will
automatically generate a posted journal entry for the production cost.

## What to do

1. Go to **Manufacturing -> Manufacturing Orders**, find and open the
   MO **M-BENCH-ACC-001**.
2. Click **Produce** in the form header, then click **Mark as Done**
   (accept the default on any confirmation dialog) so the MO moves to
   the **Done** state with 5 units produced.
3. Now switch to the **Accounting** app and open **Accounting ->
   Journal Entries** (the Journal Entries list, NOT Customer Invoices).
   Confirm that a new journal entry (`account.move`, `move_type='entry'`)
   has been auto-created for the stock move of **Bench Manuf Item** and
   is in the **Posted** state.

You do **not** need to edit, create, or post anything manually in
Accounting -- closing the MO auto-posts the entry. You only need to
**navigate** to the Journal Entries list so the agent ends on that
page.

## Rules

- Do **NOT** reduce the quantity to produce below 5.
- Do **NOT** modify or delete any component lines or the BoM.
- Do **NOT** cancel, reset, or unlink the manufacturing order.
- Do **NOT** create a backorder -- produce the full 5 units in one go.
- Do **NOT** manually create, edit, or post any journal entry -- the
  entry is created automatically when the MO is closed.
