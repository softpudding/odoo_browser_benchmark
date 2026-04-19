# Create vendor bill from scratch, post it, and pay in full

You are in the Odoo 19 **Accounting** app logged in as **Administrator**.

Create a brand-new vendor bill from scratch, post it, then register a
**full payment** against it — all in the same sitting.

## What to do

1. Open the **Accounting** app, then go to **Vendors → Bills**.
2. Click the **New** button (top-left) to start a fresh vendor bill form.
3. Fill the bill header:
   - **Vendor**: `Bench Bill Vendor`
   - **Bill Date**: `05/10/2026` (May 10, 2026)
   - **Bill Reference**: `BENCH-VBILL-001`
4. Add exactly one invoice line:

   | Product             | Quantity | Unit Price |
   |---------------------|----------|------------|
   | Bench Bill Item     | 2        | 75.00      |

   (If the Product column is not visible in the lines table, enable it
   via the optional-columns gear.)
5. Click the **Confirm** button in the header to post the bill. The
   status should flip from `Draft` to `Posted` and a number like
   `BILL/2026/...` will be assigned.
6. After posting, a **Pay** button appears in the header. Click it.
7. A **Register Payment** wizard modal opens. **Leave every field at
   its default** (full amount, today's date, Bank journal, Manual
   method, auto-filled memo).
8. Click the primary **Create Payment** button in the wizard footer. Do
   NOT click **Discard**.

## Expected end state

- A new `account.move` with `move_type = 'in_invoice'` exists for vendor
  `Bench Bill Vendor`, bill `ref = 'BENCH-VBILL-001'`, in state
  `posted`, with `payment_state = 'paid'`.
- Exactly one line on the bill: product `Bench Bill Item`, `quantity = 2`,
  `price_unit = 75.00`, `amount_total = 150.00`.
- Exactly one `account.payment` linked to that bill, with
  `amount = 150.00`, `payment_type = 'outbound'`, `partner_id = Bench
  Bill Vendor`, and its state is `posted`, `paid`, or `in_process`.

## Rules

- The bill MUST be created fresh via **New** — do not edit any existing
  bill.
- Add exactly ONE product line — no phantom empty lines, no extras.
- Use the EXACT values above for Vendor, Bill Date, Reference, quantity,
  and unit price.
- The bill MUST end posted AND paid — do not leave it as Draft, do not
  leave it Posted/Not Paid.
- Do NOT edit the amount in the payment wizard — pay the full 150.00
  (accept the wizard's default).
- Do NOT click Discard in the payment wizard.
- Do NOT create a second payment, a credit note, or any refund.
- Do NOT reset the bill to draft or cancel it after paying.
