# Adjust physical inventory counts and apply the moves

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

A warehouse clerk has just finished a physical count of two of our products
at `WH/Stock`. The system on-hand quantities are slightly off from the
physical count and must be corrected.

## Background state

Two storable products exist at `WH/Stock`:

| Product       | System On Hand | Counted (physical) |
|---------------|----------------|--------------------|
| Bench Prod A  | 20             | 18                 |
| Bench Prod B  | 15             | 16                 |

Both products appear in the **Physical Inventory** list at
**Inventory > Operations > Physical Inventory**.

## What to do

1. Open the **Inventory** app.
2. Navigate to **Operations > Physical Inventory**.
3. In the inline list, locate the row for **Bench Prod A** at location
   `WH/Stock`. Click its **Counted Quantity** cell and change the value
   from `20` to **`18`**. Press Tab (or click outside) so the edit commits.
4. Locate the row for **Bench Prod B** at location `WH/Stock`. Click its
   **Counted Quantity** cell and change the value from `15` to **`16`**.
   Press Tab (or click outside) so the edit commits.
5. Click **Apply All** in the list header (or, if you prefer, click the
   per-row **Apply** action on each row). Odoo will post an inventory
   adjustment that brings on-hand to the counted values and creates
   `stock.move` records of type *inventory adjustment* for the deltas
   (-2 for Bench Prod A, +1 for Bench Prod B).
6. If a small **"Inventory Adjustment Reference"** or **"Update
   Quantities"** confirmation dialog appears, confirm it (primary button,
   e.g. `Apply` / `Update Quantities`).

## Rules

- After applying, `stock.quant.quantity` for **Bench Prod A** at `WH/Stock`
  MUST be **18** and for **Bench Prod B** at `WH/Stock` MUST be **16**.
- Exactly one `stock.move` with `is_inventory=True` MUST exist for
  Bench Prod A (delta -2) and one for Bench Prod B (delta +1).
- Do NOT change the **On Hand Quantity** column directly by hand — only
  edit the **Counted Quantity** column and then Apply.
- Do NOT change the location of either product.
- Do NOT adjust any other product's count. Do NOT delete any quant rows.
- Do NOT manually create `stock.move` records.
