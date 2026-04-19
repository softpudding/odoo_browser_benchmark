You are in the Odoo 19 **Purchase** app, logged in as **Administrator**.

A draft Request for Quotation is already seeded. You need to confirm it,
fully receive the goods, and leave the PO in the **3-way match ready**
state — i.e. goods received, but no vendor bill has been posted yet.

## Target record

- **Vendor**: `Bench Supplier Inc`
- **Vendor Reference**: `BENCH-RFQ-3WAY-2`
- It has **two** order lines:

  | Product                 | Ordered Qty | Unit Price |
  |-------------------------|-------------|------------|
  | Bench 3WM Bracket       | 8           | 25.00      |
  | Bench 3WM Fastener Kit  | 12          | 5.00       |

## Steps

1. From **Purchase → Orders → Requests for Quotation**, open the RFQ with
   Vendor Reference `BENCH-RFQ-3WAY-2`.
2. Click the **Confirm Order** button in the form's status bar. The
   status should flip from **RFQ** to **Purchase Order**.
3. Click the **Receive Products** smart button in the PO header (it
   shows a count of **1** and opens the auto-generated vendor receipt
   in state **Ready**).
4. On the receipt, **leave the already-filled Done quantities** (8 and
   12) unchanged — the receipt auto-fills full demand.
5. Click **Validate** in the receipt's status bar. The receipt's
   status should change to **Done**. No backorder dialog will appear
   (full receipt).

## Expected end state

- The PO `BENCH-RFQ-3WAY-2` is in status **Purchase Order** (confirmed).
- The receipt is in status **Done**, with `Bench 3WM Bracket` Done = 8
  and `Bench 3WM Fastener Kit` Done = 12.
- The PO's Billing Status is **Waiting Bills** (`invoice_status = 'to
  invoice'`) — meaning the receipt is registered and a vendor bill
  could now be created, but you must NOT create or post any bill.

## Rules

- Do NOT change vendor, ordered quantities, or unit prices.
- Do NOT change the Done quantities on the receipt — the auto-filled
  full demand is correct.
- Do NOT create a backorder; the receipt covers the full demand.
- Do NOT click **Create Bills** / **Create Bill** anywhere.
- Do NOT register a payment.
- Do NOT cancel the PO or the receipt.
