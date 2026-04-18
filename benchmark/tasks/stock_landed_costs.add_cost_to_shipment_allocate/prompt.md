# Add freight landed cost to completed receipt and allocate

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

Our logistics team just paid a **45.00 EUR** freight invoice for import
receipt `R-BENCH-LC-001` (3 units of **Bench Import Item**, already
validated). You must record this as a landed cost and allocate it across
the three units so the product's stock valuation picks up the extra
freight.

## Background state

- **Completed receipt**: `R-BENCH-LC-001` (source document
  `P-BENCH-LC-001`, vendor `Bench Import Vendor`, state **Done**), 3
  units of `Bench Import Item` already transferred into stock.
- **Landed-cost service product**: `Freight` (type Service, flagged as
  "Is a Landed Cost", default split method **By Quantity**). The
  product already exists in the database; do NOT create a new one.

The `Bench Import Item` product is configured with FIFO costing and
periodic valuation so the landed cost will update the stock move's
value without touching the accounting journal.

## What to do

### Part A — Open the Landed Costs list and create a new record

1. From the Inventory app, open **Operations > Landed Costs** in the
   side menu.
2. Click **New** to open a blank landed-cost form.

### Part B — Pick the completed receipt in the Transfers field

3. In the **Transfers** many-tags field, click the input, type
   `R-BENCH-LC-001`, and select the matching entry from the
   autocomplete dropdown. This MUST be the Done receipt for the
   `Bench Import Vendor` import, not any other transfer.

### Part C — Add the Freight cost line

4. In the **Additional Costs** tab (default), click **Add a line** in
   the Cost Lines editable list.
5. In the new line:
   - **Product**: `Freight` (pick it from the autocomplete — the list
     is already filtered to landed-cost products).
   - Confirm **Split Method** is **By Quantity** (the Freight product
     ships this as its default; leave it as **By Quantity** — do NOT
     change it to Equal / By Weight / By Volume).
   - **Cost**: change the default to **45.00**.

### Part D — Compute, then Validate

6. Below the cost-lines list, click the **Compute** button. This
   generates the valuation adjustment lines in the **Valuation
   Adjustments** tab (one line of 15.00 EUR for the single
   `Bench Import Item` move, because 45 EUR / 3 units = 15 EUR/unit,
   multiplied by 3 gives 45 EUR allocated).
7. Now click the header **Validate** button. The state moves to
   **Posted**, and the original receipt's stock move cost is bumped
   to reflect the freight.

## Rules

- The landed cost record MUST end in state **Posted** (internal
  value `done`).
- There MUST be exactly **one** cost line on the record, for product
  `Freight`, with `price_unit = 45.00` and `split_method = by_quantity`.
- There MUST be exactly **one** valuation adjustment line, linked to
  the `Bench Import Item` stock move, with `quantity = 3.0` and
  `additional_landed_cost = 45.00`.
- You MUST click **Compute** BEFORE **Validate**. Clicking Validate
  on an empty adjustment table raises "Cost and adjustments lines do
  not match" and the landed cost stays in Draft.
- Do NOT create or modify the `Bench Import Item` product, the
  `Freight` product, the vendor, the PO, or the receipt. Only touch
  the new `stock.landed.cost` record.
- Do NOT pick any transfer other than `R-BENCH-LC-001`.
- Do NOT change the Split Method away from **By Quantity** — the
  check expects the cost to be allocated by the 3-unit quantity,
  not by weight/volume/equal.
