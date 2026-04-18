# Cancel the wrong receipt and create a serial-tracked replacement

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

The receiving team noticed that the vendor **Bench Supplier Inc** actually
shipped us serial-tracked widgets, NOT the item listed on the existing receipt.
You must **cancel the existing receipt** and **create a new receipt** for the
correct product.

## Background state

A **Ready** (status: Ready) vendor receipt exists with:

- **Reference / Source Document**: `R-BENCH-CANCEL-001`
- **Vendor**: `Bench Supplier Inc`
- **Product**: `Bench Hardware Item`, demand quantity **5**

## What to do

### Part A — Cancel the wrong receipt

1. Open the **Inventory** app and go to the **Receipts** transfers list
   (e.g. Operations > Transfers, filtered to Receipts, or click the
   Receipts kanban tile on the Inventory overview).
2. Open the receipt whose Source Document is `R-BENCH-CANCEL-001`.
3. In the form header, click **Cancel** so the picking moves to the
   **Cancelled** state.

### Part B — Create the replacement receipt

4. Still in the Receipts view, create a **new** receipt (click **New**).
5. On the new receipt:
   - Set the **Receive From** (vendor) field to `Bench Supplier Inc`.
   - In the **Operations** tab / lines, add one line:
     - Product: `Bench Serial Widget`
     - Demand: `2`
6. Click **Save** (or let the form auto-save when you click the header
   action).
7. Click **Mark as Todo** (or the equivalent "Confirm" header button that
   appears while the picking is in Draft) to move the picking to Ready /
   Confirmed. Dismiss any stock availability warnings by continuing.

### Part C — Enter the two serials in Detailed Operations

8. On the move line for `Bench Serial Widget`, click the **Details**
   button at the right of the line to open the **Detailed Operations**
   popup (a modal listing `stock.move.line` rows).
9. The popup starts with at most one empty move-line row. **Add a second
   move-line row** using the **Add a line** button in the popup's list
   so there are exactly **two rows**.
10. Enter the serial numbers — one per row:
    - Row 1: Lot/Serial Number = `BS-001`, Quantity = `1`
    - Row 2: Lot/Serial Number = `BS-002`, Quantity = `1`

    When the autocomplete shows `Create "BS-001"` / `Create "BS-002"`,
    pick the Create option to create the serial on the fly.
11. Click **Save** / close the popup.

### Part D — Validate

12. Back on the picking form, click **Validate** in the header.
13. The picking state should become **Done**.

## Rules

- The original picking `R-BENCH-CANCEL-001` MUST end in state **Cancelled**.
  Do not unlink/delete it.
- The replacement receipt MUST have vendor `Bench Supplier Inc` and one
  line for **`Bench Serial Widget`** only, with demand **2**.
- There MUST be **two** `stock.move.line` rows, each with Quantity `1`,
  bearing serials `BS-001` and `BS-002` exactly (no extra whitespace, no
  alternate spelling).
- Do NOT create any backorder.
- Do NOT modify or re-activate the cancelled original receipt.
- Do NOT change the demand quantity `2` on the replacement line.
