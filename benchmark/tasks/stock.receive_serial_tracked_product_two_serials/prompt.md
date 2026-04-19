# Receive a serial-tracked product with two serial numbers

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

A delivery truck from vendor **Bench Serial Vendor** has arrived at the
warehouse with **2** units of the serial-tracked product `Bench Serial Item`.
Each unit is a distinct physical unit and must be receipted with its own
serial number. You need to enter both serial numbers in the receipt's
**Detailed Operations** popup and validate the transfer.

## Background state

A **Ready** (reserved / assigned) incoming receipt picking already exists:

- **Reference / Name**: `WH/IN/BENCH-SERIAL`
- **Vendor (Receive From)**: `Bench Serial Vendor`
- **Operation Type**: `Receipts` (incoming)
- **Single move line**: `Bench Serial Item` (tracking = **Serial**), Demand **2**

The product is serial-tracked, so Validate will **refuse** until every unit
carries a distinct lot/serial number.

## What to do

1. Open the **Inventory** app and navigate to the **Receipts** transfers
   list (click the **Receipts** kanban tile on the Inventory overview, or
   use Operations > Transfers filtered to Receipts).
2. Open the receipt whose reference is `WH/IN/BENCH-SERIAL`.
3. On the `Bench Serial Item` move line, click the **Details** button at the
   right of the line (the list-row icon, tooltip "Details", which opens
   the **Detailed Operations** popup — a modal listing `stock.move.line`
   rows).
4. Inside the popup, make sure there are exactly **two** move-line rows.
   If only one row is present, click **Add a line** in the popup's list to
   add the second row.
5. Enter the serial numbers — one per row — and quantity `1` each:
   - **Row 1**: Lot/Serial Number = `SN-BENCH-A001`, Quantity = `1`
   - **Row 2**: Lot/Serial Number = `SN-BENCH-A002`, Quantity = `1`

   When the autocomplete dropdown shows `Create "SN-BENCH-A001"` /
   `Create "SN-BENCH-A002"`, pick the **Create** option so the serial is
   created on the fly.
6. Click the footer **Save** button of the popup (the primary button) to
   close the dialog. If there is a third empty row left behind after
   tabbing, delete it with the trash icon before saving.
7. Back on the picking form, click **Validate** in the header.
8. The picking state should become **Done**.

## Rules

- The receipt `WH/IN/BENCH-SERIAL` MUST end in state **Done**.
- There MUST be exactly **two** `stock.move.line` rows on the
  `Bench Serial Item` move, each with Quantity `1`, bearing serial
  numbers `SN-BENCH-A001` and `SN-BENCH-A002` exactly (no extra
  whitespace, no alternate spelling).
- Two `stock.lot` records MUST be created for `Bench Serial Item` with
  those two names — not one lot of quantity 2.
- Do NOT change the Demand quantity (`2`) on the move line.
- Do NOT cancel or unlink the receipt.
- Do NOT create any backorder.
- Do NOT add any extra products or pickings.
