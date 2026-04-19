# Receive a PO in two batches, scrap the damaged units, and finish it

Open the **Purchase** app. There is a confirmed purchase order from vendor
**Bench Harbor Supply** with source document **`SCRAP-PO-07`**.

It contains these two lines:

| Product                 | Ordered Qty |
|-------------------------|-------------|
| Bench Control Valve     | 6           |
| Bench Filter Cartridge  | 10          |

You need to receive the goods in two batches, scrap one damaged filter from the
first receipt, and finish the order correctly.

## Batch 1 — Partial receipt

1. Open the PO and go to its receipt.
2. In the receipt, set the **Done** quantities to:
   - `Bench Control Valve`: `4`
   - `Bench Filter Cartridge`: `7`
3. Click **Validate**.
4. When Odoo asks about the remaining quantities, choose
   **Create Backorder**.

## Scrap the damaged unit

5. Stay on the first completed receipt and use the **Scrap** action / button.
6. Scrap exactly **1** unit of **`Bench Filter Cartridge`** from the receipt.
   Keep the default scrap location.
7. Validate the scrap.

## Batch 2 — Finish the backorder

8. Open the backorder receipt for the remaining quantities.
9. Receive the rest of the order:
   - `Bench Control Valve`: `2`
   - `Bench Filter Cartridge`: `3`
10. Validate the backorder receipt.

## Rules

- Create exactly one scrap record.
- Scrap only `Bench Filter Cartridge`, quantity `1`.
- Do not cancel the PO or either receipt.
- The PO line ordered quantities must stay at `6` and `10`.
- Both receipts must end in **Done**.
