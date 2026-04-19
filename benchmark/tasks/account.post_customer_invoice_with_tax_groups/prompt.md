# Create a customer invoice, apply the 20% sale tax, and post it

You are in the Odoo 19 **Accounting** app logged in as **Administrator**.

Create a brand-new **customer invoice** from scratch with a single line
using the **20%** sale tax (NOT the 10% one), and post it.

## What to do

1. Open the **Accounting** app, then go to **Customers -> Invoices**.
2. Click the **New** button (top-left) to start a fresh customer invoice form.
3. Fill the invoice header:
   - **Customer**: `Bench Tax Cust`
   - **Invoice Date**: `05/10/2026` (May 10, 2026)
4. Add exactly one invoice line on the **Invoice Lines** tab:

   | Product             | Quantity | Unit Price | Taxes                 |
   |---------------------|----------|------------|-----------------------|
   | Bench Tax Service   | 1        | 200.00     | Bench Sale Tax 20%    |

   The **Taxes** cell is a many2many tag widget (pills). Click into it,
   type `Bench Sale Tax 20%`, and pick it from the autocomplete dropdown
   so the pill appears in the cell.

   Two taxes exist that look similar:
   - `Bench Sale Tax 10%`  -- DO NOT pick this one.
   - `Bench Sale Tax 20%`  -- this is the correct one.

   If any other tax pill is pre-filled in the Taxes cell (for example a
   leftover default), remove it by clicking its `x` icon so only
   `Bench Sale Tax 20%` remains.
5. Click the **Confirm** button in the header (statusbar) to post the
   invoice. The status should flip from `Draft` to `Posted` and a number
   like `INV/2026/...` will be assigned.

## Expected end state

- A new `account.move` with `move_type = 'out_invoice'` exists for
  customer `Bench Tax Cust`, `invoice_date = 2026-05-10`, state
  `posted`.
- Exactly one invoice line: product `Bench Tax Service`, `quantity = 1`,
  `price_unit = 200.00`, with `tax_ids` containing **only**
  `Bench Sale Tax 20%` (not the 10%).
- Invoice totals: `amount_untaxed = 200.00`, `amount_tax = 40.00`,
  `amount_total = 240.00`.

## Rules

- The invoice MUST be created fresh via **New** -- do not edit any
  existing invoice.
- Add exactly ONE product line -- no phantom empty lines, no extras.
- Use the EXACT values above for Customer, Invoice Date, Product,
  Quantity, Unit Price, and Tax.
- The line's **Taxes** column must contain **Bench Sale Tax 20%** only
  -- NOT the 10% tax, NOT both taxes.
- The invoice MUST end **posted** -- do not leave it in Draft.
- Do NOT cancel, reset to draft, or delete the invoice after posting.
