"""Oracle for account_followup.send_reminder_level_two_customers.

BLOCKED TASK — the Follow-up Reports / Customer Statement screen is
shipped by the Enterprise-only `account_followup` addon, which is NOT
vendored in this Odoo 19 Community checkout. The oracle exits with a
clear error so the harness records the blocker instead of producing
spurious results.

To flesh out once the enterprise account_followup addon is vendored:
  1. Navigate to `/odoo/action-account_followup.action_account_manual_followup`
     (or Accounting → Customers → Follow-up Reports from the menu).
  2. Expect a list of customers-with-overdue-balances. Search for
     'Bench Overdue Co' and click the row.
  3. Expect the per-customer follow-up card with:
       - Breadcrumb 'Follow-up Reports > Bench Overdue Co'
       - 3 invoice rows (OV/BENCH/001..003) visible, all 45d overdue.
       - Header reminder-level chip reading 'Second Reminder'.
       - Header buttons: 'Send Email' (primary) / 'Send Letter' /
         'Schedule Activity' / 'Done' / 'Remind Later'.
  4. Click header 'Send Email'. A small confirmation dialog with the
     rendered email preview may appear — if so, click 'Send' in the
     footer. Otherwise Odoo fires the mail directly and shows a success
     toast 'Email sent'.
  5. After sending, reload the card and assert:
       - Chatter on the partner now has a new message whose body
         contains all three invoice names.
       - Header reminder-level state advanced ('followup_status' went
         from 'in_need_of_action' to 'with_overdue_invoices' or similar
         — the exact flag depends on Enterprise version).

Typical selectors on the Enterprise follow-up report:
  - `.o_followup_report` — root container for the per-customer card.
  - `.o_followup_line_header_name` — partner name in card header.
  - `.o_followup_report_infos` — level / overdue summary chip.
  - `button[name='action_send_mail']` — header 'Send Email' button.
  - `.o_followup_report_o_form_button_primary` — primary footer action
    on the preview modal.

Selector names have shifted between Odoo versions — confirm against
the current enterprise source before writing selectors.
"""

from benchmark.oracle_helpers import run_oracle


def oracle(page):
    raise RuntimeError(
        "BLOCKED: the Follow-up Reports screen "
        "(/odoo/action-account_followup.action_account_manual_followup) is "
        "not available in this Odoo 19 Community checkout "
        "(Enterprise-only). Oracle body intentionally short-circuits. "
        "See STATUS.md row 404."
    )


run_oracle(oracle)
