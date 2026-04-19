"""Oracle for account.refund_customer_invoice_cash_basis.

Open posted single-line invoice BENCH-REFUND-001 for Bench Ref Co,
click the statusbar "Credit Note" button (which opens the
account.move.reversal wizard), fill reason "Cash basis partial refund",
leave the default (today) date and default journal, click primary
"Reverse" (refund_moves — NOT "Reverse and Create Invoice"), then on the
generated draft out_refund change the lone copied line's price_unit
from 500 to 200, and post the credit note via the header Confirm.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    modal_fill_field,
    navigate,
    run_oracle,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Open the posted single-line invoice.
    click_list_row(page, "BENCH-REFUND-001")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # On customer invoices, the reversal wizard button in the statusbar
    # is labeled "Credit Note".
    click_status_button(page, "Credit Note")
    page.wait_for_timeout(1500)
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(800)

    # Fill reason; leave date + journal at defaults.
    modal_fill_field(page, "reason", "Cash basis partial refund")
    page.wait_for_timeout(500)

    # Primary refund button. Must NOT click "Reverse and Create Invoice"
    # (name=modify_moves) which creates a second draft invoice.
    modal = page.locator(".modal:visible").last
    reverse_btn = modal.locator(
        "button.btn-primary[name='refund_moves']"
    ).first
    if reverse_btn.count() == 0:
        # Fallback: match by exact visible text.
        buttons = modal.locator("footer button")
        picked = None
        for i in range(buttons.count()):
            b = buttons.nth(i)
            if b.inner_text().strip() == "Reverse":
                picked = b
                break
        if picked is None:
            raise AssertionError("Could not locate primary 'Reverse' button")
        reverse_btn = picked
    reverse_btn.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # We are now on the draft credit note (out_refund) with one copied
    # line (Bench Refund Service, qty=1, price_unit=500). Override
    # price_unit to 200 in-place — do NOT delete the row or add new rows.
    set_o2m_field(page, 0, "price_unit", "200")
    page.wait_for_timeout(900)
    _wait_no_loading(page)

    # Post the credit note via the header Confirm button.
    click_status_button(page, "Confirm")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
