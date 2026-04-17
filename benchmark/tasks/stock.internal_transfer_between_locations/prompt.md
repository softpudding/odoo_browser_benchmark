# Validate an internal transfer between locations

You are in the Odoo 19 **Inventory** app logged in as **Administrator**.

An **Internal Transfer** has already been prepared to move 5 units of
**Benchmark Shelf Widget** from **WH/Stock** to **WH/Stock/Shelf A1**.
It is sitting in the Internal Transfers queue waiting for you to set
the done quantity and validate it.

## What to do

1. Open the **Inventory** app.
2. Click the **Internal Transfers** operation card.
3. Open the pending transfer with origin reference **BENCH-INT-SHELF-A1**.
4. On the move line, set the done **Quantity** to **5** (matching the
   demand).
5. Click **Validate**. If a confirmation dialog appears (e.g. "Apply"),
   accept the default.

The transfer should end in the **Done** state.

## Rules

- Validate **exactly one** transfer — the one with origin
  `BENCH-INT-SHELF-A1`.
- Do **not** cancel or delete the transfer.
- Do **not** modify its source or destination location.
- Do **not** create additional transfers.
