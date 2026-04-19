# Create a putaway rule for Bench Putaway Item

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

A new storable product **`Bench Putaway Item`** has been added to the
catalog, and a new sub-location **`WH/Stock/Shelf B`** has been created
under the main warehouse stock location. Create a putaway rule so that
whenever **`Bench Putaway Item`** arrives in **`WH/Stock`**, it is
automatically routed to **`WH/Stock/Shelf B`**.

## What to do

1. Open the **Inventory** app.
2. Navigate to **Configuration → Putaway Rules** (in the top menu).
3. On the Putaway Rules list, click **New** to open a fresh inline row at
   the bottom of the list.
4. In the new row fill **exactly these three fields**:
   - **When product arrives in** (source) = `WH/Stock`
   - **Product** = `Bench Putaway Item`
   - **Store to** (destination) = `WH/Stock/Shelf B`
5. Leave the Product Category column empty — this is a **product-level**
   rule, not a category-level rule.
6. Leave Storage Category, Package Type, Priority and Company at their
   defaults.
7. Save the list (click the cloud/save icon in the breadcrumb, or press
   Tab off the last cell and then click Save) so the new
   `stock.putaway.rule` is persisted.

## Rules

- Exactly ONE new `stock.putaway.rule` must exist after the task, with
  `product_id = Bench Putaway Item`, `location_in_id = WH/Stock`,
  and `location_out_id = WH/Stock/Shelf B`.
- The rule must be **product-based**. Fill the **Product** column; leave
  the **Product Category** column empty.
- Do NOT swap source and destination. `WH/Stock` is the source, and
  `WH/Stock/Shelf B` is the destination.
- Do NOT create the rule via the product form's putaway smart button or
  any other entry point — you must reach the list via
  **Configuration → Putaway Rules**.
- Do NOT modify the product, the locations, the warehouse, or any other
  existing putaway rule.
- Do NOT leave a blank/draft putaway rule behind with no product and no
  category.
