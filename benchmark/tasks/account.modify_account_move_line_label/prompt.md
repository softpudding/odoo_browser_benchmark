# Fix the label on a posted customer invoice line

You are in the Odoo 19 **Accounting** app logged in as **Administrator**.

A posted customer invoice has a single line whose **Label** text is wrong and
needs to be corrected. Accounting won't let you edit a posted invoice line
directly — you must reset the invoice to draft, fix the label, then re-post.

| Customer        | Reference        | Total  | Status |
|-----------------|------------------|--------|--------|
| Bench Edit Co   | `BENCH-EDIT-001` | 100.00 | Posted |

The invoice has **one** line with:
- Label: `Service`  ← this is wrong
- Unit Price: 100.00
- Quantity: 1

## What to do

1. From the **Accounting** app, go to **Customers → Invoices**.
2. Open the invoice with reference **`BENCH-EDIT-001`** (customer
   **Bench Edit Co**). Verify its status is `Posted`.
3. In the invoice header, click the **Reset to Draft** button. The
   status should flip from `Posted` back to `Draft` and the line fields
   become editable.
4. On the **single** invoice line, edit the **Label** column from
   `Service` to exactly:

   > Corrected description

   Do **NOT** change the Product, Quantity, or Unit Price — only the
   Label (the `name` field of the invoice line).
5. After editing the label, click the **Confirm** button in the header
   to re-post the invoice. The status must end as `Posted` again.

## Expected end state

- Invoice `BENCH-EDIT-001` is in state **Posted**.
- The single invoice line's label (`name`) is exactly
  `Corrected description`.
- The invoice's `amount_total` is still **100.00** (no price or
  quantity change).

## Rules

- You MUST click **Reset to Draft** before editing the line — a posted
  invoice line's label is not editable otherwise.
- You MUST click **Confirm** after editing — leaving the invoice in
  draft counts as failure.
- Only the **Label** field of the single invoice line may change.
  Do NOT change the Product, Quantity, Unit Price, Account, Taxes, or
  Partner.
- Do NOT create or delete lines. The invoice must still have exactly
  one product line after your edit.
- Do NOT cancel the invoice at any point.
