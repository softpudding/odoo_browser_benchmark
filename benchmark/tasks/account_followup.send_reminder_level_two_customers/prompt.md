# Send a level-2 follow-up reminder to overdue customers (BLOCKED)

> **Note**: This task is BLOCKED because the `account_followup` addon is an
> **Odoo Enterprise** module that is NOT vendored in this Odoo 19
> Community checkout. The Follow-up Reports screen, the
> **Customer Statement** action, the per-customer follow-up card with
> the header **Send Email** / **Send Letter** / **Schedule Activity**
> buttons, and the `account_followup.followup.line` level configuration
> all ship exclusively in the Enterprise `account_followup` addon.
>
> What is present in Community:
> - `addons/account/` — `account.move`, `account.move.line`,
>   `account.payment`, etc. but NO per-partner follow-up workflow. The
>   only related artefact is the `send_invoices_followups` upgrade
>   boolean on Accounting Settings, which installs the separate
>   `snailmail_account` addon (physical-mail invoicing), NOT a follow-up
>   workflow.
> - `addons/mail/` — `mail.mail`, `mail.message`, chatter `Send Message`
>   button. These are the primitives the Enterprise follow-up report
>   uses under the hood, but the **Send Email** button on a customer's
>   follow-up card, the default level-based reminder template, and the
>   auto-attach of overdue invoice PDFs are all implemented in the
>   absent `account_followup` module.
>
> There is no `account_followup` directory under `addons/`, no
> `account_followup.followup.line` model, no
> `account_followup.followup.report` client action, no
> `/odoo/action-account_followup.*` route, and no
> `account_followup_manual_reminder` wizard in this codebase.
> `grep -rn "account_followup" addons/` returns zero matches.
>
> The original task intent is preserved below for future re-scoping
> when the enterprise addon is vendored.

You will send a level-2 payment reminder to a customer with overdue
invoices, using the Follow-up Reports screen.

## Phase 1 — Open Follow-up Reports

1. Navigate to **Accounting** → **Customers** → **Follow-up Reports**
   (or Customer Statement, depending on menu labels).
2. From the list of customers with unpaid balances, open the card for
   **Bench Overdue Co**.

## Phase 2 — Trigger the reminder

3. On the follow-up card, confirm the three seeded posted invoices
   (each 45 days past due, totalling an "Amount Overdue" > 0) are
   pre-selected in the table.
4. Confirm the **Follow-up Status / Level** shows `Second Reminder`
   (default level 2 — Odoo auto-escalates based on days-overdue).
5. Click the header **Send Email** button (it uses the default level-2
   reminder template).

## Phase 3 — Verify

6. After the follow-up is sent, the card should show:
   - `next_action_date` updated to today + level 2 delay.
   - A chatter message logged on **Bench Overdue Co** referencing each
     of the 3 invoice names.
   - At least one `mail.mail` / `mail.message` record addressed to
     the partner's email with a body referencing the invoices.

## Rules

- Final state: `res.partner` with name `Bench Overdue Co` has
  `followup_status` advanced (field specific to `account_followup`).
- At least one `mail.message` is logged on the partner record whose
  body mentions all three invoice names (`OV/BENCH/001`,
  `OV/BENCH/002`, `OV/BENCH/003`).
- All three invoices remain `state=='posted'` and
  `payment_state=='not_paid'` (follow-up does not touch invoice
  state, only sends a reminder).
