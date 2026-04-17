# Internal transfer from stock to shelf location

You are in the Odoo 19 **Inventory** app logged in as **Administrator**.

Five units of **Benchmark Shelf Widget** need to be moved from the
main **WH/Stock** location to a dedicated shelf **WH/Stock/Shelf A1**
for staging before shipping. Create and validate an **Internal Transfer**
to complete the move.

## What to do

1. Open the **Inventory** app.
2. On the Operations dashboard, find the **Internal Transfers** card
   (for the main warehouse) and click **New** to create a new internal
   transfer. *(If you start elsewhere, use **Operations → Transfers**
   and pick the Internal Transfers operation type.)*
3. Fill in:
   - **Source Location**: `WH/Stock`
   - **Destination Location**: `WH/Stock/Shelf A1`
   - **Reference / Origin**: `BENCH-INT-SHELF-A1`
4. In the Operations / Detailed operations tab, add one line:
   - **Product**: `Benchmark Shelf Widget`
   - **Demand** (quantity): `5`
5. Click **Confirm** (mark as ready), set the **done quantity** to `5`
   for that line, and click **Validate** to transfer the stock.
6. The transfer should end in the **Done** state.

## Rules

- Source location must be `WH/Stock`, destination must be
  `WH/Stock/Shelf A1`.
- The transfer must have the origin `BENCH-INT-SHELF-A1`.
- Exactly one product line must be present: 5 units of
  **Benchmark Shelf Widget**.
- Final state must be **Done** (validated).
- Do **not** create other transfers.
- Do **not** modify the product's fields.
