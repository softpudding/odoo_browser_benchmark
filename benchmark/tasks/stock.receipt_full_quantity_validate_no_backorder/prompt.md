# Validate a full-quantity incoming receipt (no backorder dialog)

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

A delivery truck from vendor **Bench Vendor** has arrived at the warehouse with
**10** units of `Bench Recv Item`. The receipt is already reserved and the Done
quantity matches the demand exactly — you just need to confirm the goods have
been put away by validating the receipt.

## Background state

A **Ready** (reserved / assigned) incoming receipt picking already exists:

- **Reference / Name**: `WH/IN/BENCH-FULL`
- **Vendor (Receive From)**: `Bench Vendor`
- **Operation Type**: `Receipts` (incoming)
- **Single move line**: `Bench Recv Item`, Demand **10**, Quantity (Done) **10**
  (fully reserved — the picker has already put away all 10 units)

Because Quantity (Done) exactly matches Demand, **no backorder dialog will
appear** when you click Validate. The picking should flip straight to
**Done**.

## What to do

1. Open the **Inventory** app and navigate to the **Receipts** transfers list
   (click the **Receipts** kanban tile on the Inventory overview, or use
   Operations > Transfers filtered to Receipts).
2. Open the receipt whose reference is `WH/IN/BENCH-FULL`.
3. In the header, click **Validate**.
4. The picking state should become **Done**. No dialog should appear.

## Rules

- The receipt `WH/IN/BENCH-FULL` MUST end in state **Done** with the single
  Bench Recv Item move reporting Quantity (Done) = **10**.
- **NO backorder** `stock.picking` may exist — after Validate there must be
  zero pickings whose `backorder_id` equals the original's id (since Done
  already matches Demand, Odoo should not prompt for a backorder at all).
- On-hand stock at `WH/Stock` for `Bench Recv Item` MUST be **10** after
  validation (the goods are now in stock).
- Do NOT change Quantity (Done) or Demand on the move line — they are already
  correct.
- Do NOT cancel or unlink the receipt.
- Do NOT add extra products, extra lines, or extra pickings.
