Go to the **Sales** app and open **Quotations**.

Find the draft quotation **BENCH-CONFIRM** for customer **Bench Confirm Co**
and open it.

The quotation has **one** order line on the **Order Lines** tab:

| Line | Product | Qty | Unit Price |
|---|---|---|---|
| 1 | Bench Confirm Item | 1 | 100.00 |

Your task: **convert this quotation into a confirmed Sales Order** by
clicking the **Confirm** button in the quotation's status bar (header).

Steps:

1. On the opened quotation, click the **Confirm** button in the status bar
   (the header, next to the Quotation → Sales Order stage indicator).
2. The status bar should flip from **Quotation** to **Sales Order** and
   the internal state must become `sale` (confirmed).

**Rules:**

- Do NOT change the customer, product, quantity, or unit price.
- Do NOT add, remove, or modify any order lines.
- Do NOT cancel or delete the quotation.
- Do NOT create a new quotation — use the existing **BENCH-CONFIRM**
  record.
- A single click on **Confirm** is all that is required; if Odoo opens an
  information dialog (e.g. about a company-level warning) just dismiss it
  with OK / Confirm.
