# Attach the invoice PDF to the customer invoice's chatter

You are in the Odoo 19 **Accounting** app logged in as **Administrator**.

A **posted** customer invoice exists. The finance team wants the invoice
PDF report attached to the invoice's **chatter** (the Communication panel
on the right of the invoice form) so it is linked to the record alongside
the email thread to the customer.

| Customer | Reference | Total | Status |
|----------|-----------|-------|--------|
| Bench Print Co | `BENCH-PRINT-001` | 150.00 | Posted |

## What to do

1. Open the **Accounting** app, then go to **Customers → Invoices**.
2. Open the invoice with reference **`BENCH-PRINT-001`** (customer
   **Bench Print Co**). Verify its status is **Posted**.
3. In the invoice form **header**, click the **Send** button. A dialog
   titled **"Send"** opens (the Send & Print wizard).
4. The dialog is pre-filled — leave all defaults as-is:
   - The **To** field already contains the customer
     (`billing@benchprint.example.com`).
   - The **by Email** sending method is already ticked.
   - The **Subject** and email **body** are pre-filled from the invoice
     template.
   - The invoice **PDF** is already listed under the attachment strip at
     the bottom of the dialog.
5. Click the primary **Send** button at the bottom-left of the dialog
   (the blue button labelled "Send"). **Do NOT click Discard.**

When the dialog closes the invoice's chatter must show a new outgoing
email message whose attachments include the invoice PDF (file name
ending in `.pdf`).

## Why Send (not the header Print button)

- The header has a stand-alone **Print** button too. That button only
  downloads / previews the PDF in a new browser tab — it does NOT post
  any chatter message and does NOT link the PDF to the invoice's
  Communication panel. Clicking that button alone is NOT enough for
  this task.
- The chatter-attach happens only as a side effect of the **Send & Print
  wizard** dispatching the email — the wizard posts a `mail.message` on
  the invoice whose `attachment_ids` include the PDF.

## Expected end state

- Invoice `BENCH-PRINT-001` is still **Posted** (unchanged), partner
  **Bench Print Co**, total **150.00** — you MUST NOT reset to draft,
  cancel, or reverse it, and you MUST NOT edit any line.
- A chatter `mail.message` exists on the invoice carrying at least one
  attached file whose name ends with `.pdf`.

## Rules

- The invoice MUST end Posted — do not reset to draft.
- Do NOT cancel or reverse the invoice.
- Do NOT edit the partner, amount, or any invoice line.
- In the Send dialog, do NOT uncheck **Email** and do NOT click
  **Discard**.
- Only operate on `BENCH-PRINT-001` — do not send / print any other
  invoice.
