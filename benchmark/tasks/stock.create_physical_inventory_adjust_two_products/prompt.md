# Adjust the physical inventory count for two products

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

A warehouse clerk has finished a physical count of two storable products
at `WH/Stock`. The system on-hand quantities differ from the physical
count and must be corrected via Odoo's Physical Inventory adjustment
flow.

## Background state

Two storable products already exist at `WH/Stock`:

| Product       | System On Hand | Counted (physical) |
|---------------|----------------|--------------------|
| Bench Prod X  | 15             | 12                 |
| Bench Prod Y  | 25             | 27                 |

Both products appear in the **Physical Inventory** list at
**Inventory > Operations > Physical Inventory**.

## What to do

1. Open the **Inventory** app.
2. Navigate to **Operations > Physical Inventory**.
3. In the inline list, locate the row for **Bench Prod X** at location
   `WH/Stock`. Click its **Counted Quantity** cell and change the value
   from `15` to **`12`**. Press Tab (or click outside) so the edit commits.
4. Locate the row for **Bench Prod Y** at location `WH/Stock`. Click its
   **Counted Quantity** cell and change the value from `25` to **`27`**.
   Press Tab (or click outside) so the edit commits.
5. Click **Apply All** in the list header (or, if you prefer, click the
   per-row **Apply** action on each row). Odoo will post an inventory
   adjustment that brings on-hand to the counted values and creates
   `stock.move` records of type *inventory adjustment* for the deltas
   (-3 for Bench Prod X, +2 for Bench Prod Y).
6. If a small **"Inventory Adjustment Reference"** or **"Update
   Quantities"** confirmation dialog appears, confirm it (primary button,
   e.g. `Apply` / `Update Quantities`).

## Rules

- After applying, `stock.quant.quantity` for **Bench Prod X** at `WH/Stock`
  MUST be **12** and for **Bench Prod Y** at `WH/Stock` MUST be **27**.
- At least one `stock.move` with `is_inventory=True, state='done'` MUST
  exist for **Bench Prod X** (net signed delta -3 at WH/Stock) and one
  for **Bench Prod Y** (net signed delta +2 at WH/Stock).
- Do NOT change the **On Hand Quantity** column directly by hand — only
  edit the **Counted Quantity** column and then Apply.
- Do NOT change the location of either product.
- Do NOT adjust any other product's count. Do NOT delete any quant rows.
- Do NOT manually create `stock.move` records.
