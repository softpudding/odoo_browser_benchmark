# Create and validate an internal transfer

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

The warehouse team wants to move **5** units of `Bench Move Item` from the
main stock location `WH/Stock` to the sub-location `WH/Stock/Shelf C`. There
is currently **no** pending internal transfer for this move — you must create
a new one from scratch and validate it.

## Background state

- Storable product `Bench Move Item` exists with **10** units on-hand at
  `WH/Stock`.
- Sub-location `WH/Stock/Shelf C` (internal) exists under `WH/Stock`.
- Multi-location features are enabled (you have the `Storage Locations`
  group), so the Source and Destination Location pickers are visible on the
  transfer form.

## What to do

1. Open the **Inventory** app and navigate to the **Transfers** list
   (Operations > Transfers, or from the Inventory overview).
2. Click **New** (top of the list) to open a blank transfer form.
3. Set the **Operation Type** to `Internal Transfers` (the transfer type
   whose `code` is `internal`; its display name is literally
   **Internal Transfers**). The form will update to show internal Source /
   Destination Location fields.
4. Set **Source Location** to `WH/Stock`.
5. Set **Destination Location** to `WH/Stock/Shelf C`.
6. In the **Operations** tab, add exactly **one** line:
   - **Product**: `Bench Move Item`
   - **Demand**: `5`
   (Leave the `UoM` at the default `Units`. Do NOT add a second line.)
7. Click **Mark as Todo** (also labelled *Confirm* on some versions — the
   header button that confirms the draft transfer and reserves stock). The
   state should flip to **Ready** with Quantity auto-filled to `5` on the
   move line.
8. Click **Validate** in the header. Because Quantity (`5`) matches Demand
   (`5`), no Create Backorder dialog appears and the transfer goes straight
   to **Done**.

## Rules

- Exactly **one** internal `stock.picking` must exist when you are done, in
  state `done`, with source `WH/Stock`, destination `WH/Stock/Shelf C`, and
  one move line for `Bench Move Item` with Quantity (Done) = `5`.
- The new picking's `picking_type_id.code` MUST be `internal`. Do NOT pick
  Receipts or Delivery Orders.
- After validation, a `stock.quant` for `Bench Move Item` at
  `WH/Stock/Shelf C` must have quantity `5`, and the `WH/Stock` quant must
  be reduced from `10` to `5`.
- Do NOT create extra transfers, extra move lines, or extra products.
- Do NOT create or rename any locations or picking types.
- Do NOT cancel the transfer.
- If you accidentally leave a blank second Operations line, remove it before
  saving.
