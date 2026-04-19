# Post the draft invoice, then send it to the customer by email

You are in the Odoo 19 **Accounting** app logged in as **Administrator**.

A **draft** customer invoice exists and needs to be posted, then sent to the
customer by email.

| Customer | Reference | Total | Status |
|----------|-----------|-------|--------|
| Bench Post Co | `BENCH-POST-SEND-001` | 200.00 | Draft |

## What to do

1. Open the **Accounting** app, then go to **Customers → Invoices**.
2. Open the invoice with reference **`BENCH-POST-SEND-001`** (customer
   **Bench Post Co**). Verify its status is `Draft`.
3. In the invoice form header, click the **Confirm** button. The invoice
   status should flip from `Draft` to `Posted` and a number like
   `INV/.../...` will be assigned.
4. After posting, a **Send** button appears in the header. Click it.
5. A dialog titled **"Send"** opens. The dialog is already pre-filled:
   - The **To** field already contains **Bench Post Co** (`billing@benchpost.example.com`).
   - The **Subject** and email **body** are prefilled from the invoice
     template.
   - The **Email** sending method is already checked.

   Leave everything as-is and click the primary **Send** button at the
   bottom-left of the dialog. **Do NOT** click **Discard**. **Do NOT**
   uncheck Email.

## Expected end state

- Invoice `BENCH-POST-SEND-001` is in state **Posted**.
- The invoice's `is_move_sent` flag is **True** (the Send button in the
  header becomes greyed / no longer highlighted after successful send).
- At least one `mail.message` is attached to the invoice with an email
  notification (the outbound send-to-customer email).

## Rules

- The invoice MUST end posted — do not leave it in draft.
- The send dialog MUST be completed — clicking **Discard** counts as a
  failure.
- Do NOT unselect the Email sending method in the wizard.
- Do NOT change the partner, the amount, or the invoice lines.
- Do NOT reset the invoice to draft or cancel it after sending.
- Only the one invoice `BENCH-POST-SEND-001` must be touched — do not
  post or send any other draft invoice.
