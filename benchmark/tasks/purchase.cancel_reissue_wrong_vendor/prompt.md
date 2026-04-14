Open the Purchase app. There is a confirmed purchase order from vendor **Atlas Industrial** with source document `VENDOR-FIX-01`.

This PO was sent to the **wrong vendor**: it currently shows vendor **Atlas Industrial** but it should have been sent to **Pinnacle Parts**.

The PO has two lines:

| Product          | Qty | Unit Price |
|------------------|-----|------------|
| Hydraulic Pump   | 5   | 340        |
| Pressure Gauge   | 10  | 85         |

Because the PO is already confirmed, you **cannot simply edit the vendor field**. You must:

1. **Cancel** the incorrect PO (use the Cancel button).
2. **Create a new purchase order** for vendor **Pinnacle Parts** with exactly the same lines:
   - Hydraulic Pump: qty 5, unit price 340
   - Pressure Gauge: qty 10, unit price 85
3. **Confirm** the new purchase order.

**Rules:**
- The original PO to Atlas Industrial must end in Cancelled status
- The new PO to Pinnacle Parts must end in confirmed (Purchase Order) status
- Product names, quantities, and unit prices on the new PO must match exactly
- Do not delete the cancelled PO — it should remain as a record
