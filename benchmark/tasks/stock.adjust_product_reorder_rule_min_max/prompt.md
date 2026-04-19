# Add a reordering rule (Min 5 / Max 20) to Bench Reorder Item

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

A new storable product **`Bench Reorder Item`** has been added to the catalog
with on-hand = 0 at `WH/Stock`. It currently has **no reordering rule**.
Add a reordering rule so the system can propose a replenishment when stock
drops below 5 units, refilling up to 20 units.

## What to do

1. Open the **Inventory** app.
2. Go to the top menu **Products > Products** and open the product
   **`Bench Reorder Item`**.
3. On the product form, click the **Reordering Rules** smart button in the
   button box at the top of the form (it shows `0 Reordering Rules` today).
4. This opens the **Reordering Rules** list view filtered to this product.
   Click **New** to start a fresh inline row.
5. In the new row:
   - Leave **Product** at the default `Bench Reorder Item` (the smart button
     context pre-fills it — do not change it).
   - Leave **Location** at the default `WH/Stock` (visible if the Location
     column is on — the default is the main warehouse stock location).
   - Set **Min** (Min Quantity / `product_min_qty`) to `5.00`.
   - Set **Max** (Max Quantity / `product_max_qty`) to `20.00`.
6. Save the list (click the cloud/save icon in the breadcrumb, or press
   Tab off the last cell and then click Save) so the new
   `stock.warehouse.orderpoint` is persisted.

## Rules

- Exactly ONE new `stock.warehouse.orderpoint` must exist for
  `Bench Reorder Item` after the task, with `product_min_qty = 5.0`
  and `product_max_qty = 20.0`.
- The orderpoint MUST be linked to `Bench Reorder Item` and located at
  `WH/Stock` (the main warehouse stock location).
- Do NOT create the orderpoint from `Inventory > Operations > Replenishment`
  or from any other entry point — you must reach it via the product form's
  **Reordering Rules** smart button.
- Do NOT modify the product itself (do not change its name, type, or
  routes).
- Do NOT click **Order** / **Automate** / **Replenish** — the agent must
  only create the rule, not trigger a purchase order or replenishment.
- Do NOT create additional reordering rules for any other product.
