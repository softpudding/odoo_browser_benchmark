# Unbuild 2 finished Bench Assembly units back into their components

You are in the Odoo 19 **Manufacturing** app logged in as **Administrator**.

The warehouse has **2 units of `Bench Assembly`** on hand at **`WH/Stock`**.
Quality control rejected the whole batch and you must **unbuild** those 2
units so their components (Bench Screw, Bench Housing) return to stock.

The Bill of Materials for `Bench Assembly` consumes:
- **3x `Bench Screw`**
- **1x `Bench Housing`**

There is **no manufacturing order** associated with this unbuild — it's a
direct unbuild driven by the Bill of Materials.

## What to do

1. Open the **Manufacturing** app.
2. Go to **Products → Unbuild Orders** in the Manufacturing top menu
   (it lives under the **Products** menu, not under **Operations**).
3. Click **New** to create a new unbuild order.
4. Fill in the form:
   - **Product**: `Bench Assembly` — the **Bill of Material** field
     auto-populates with the only BoM for this product (leave it).
   - **Quantity**: `2`
   - **Manufacturing Order**: leave **empty** (there is no MO to link).
   - **Source Location**: leave at the default `WH/Stock`.
   - **Destination Location**: leave at the default `WH/Stock`.
5. Click the **Unbuild** button in the form status bar
   (or **Validate** / **Confirm**, depending on the label your version
   shows — it runs `action_validate`).

After the unbuild runs, the form should be in the **Done** state and the
stock movements should be:
- **2 Bench Assembly** consumed from `WH/Stock` (on-hand goes from 2 → 0).
- **6 Bench Screw** returned to `WH/Stock` (3 per unit x 2).
- **2 Bench Housing** returned to `WH/Stock` (1 per unit x 2).

## Rules

- Create **exactly one** unbuild order.
- The unbuild must be **product-driven** (no Manufacturing Order field
  set). Do **not** create or link a `mrp.production` (Manufacturing
  Order) — the form's **Manufacturing Order** field stays blank.
- Use the pre-seeded **normal** Bill of Materials for Bench Assembly —
  do **not** edit it, duplicate it, or create a new one.
- The unbuild quantity must be exactly **2** (not 1, not 3).
- The unbuild must end in the **Done** state (validated).
- Do **not** create any manufacturing orders, extra unbuild orders,
  scrap orders, or inventory adjustments.
- Do **not** change the Source Location or Destination Location away
  from `WH/Stock`.
