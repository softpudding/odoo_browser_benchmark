"""Oracle for account.pay_invoice_with_memo.

Open posted invoice BENCH-PAYMEMO-01 for Highfield Consulting, click Pay,
change Memo to Q2-2026-INV-SETTLE and Payment Date to 05/08/2026, then
click Create Payment.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    modal_click_button,
    modal_set_date,
    ensure_list_view,
    _dismiss_tooltips,
)

TARGET_REF = "BENCH-PAYMEMO-01"
MEMO = "Q2-2026-INV-SETTLE"
PAYMENT_DATE = "05/08/2026"


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    ensure_list_view(page)
    # Search by reference to uniquely identify the target invoice
    click_list_row(page, TARGET_REF)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    _dismiss_tooltips(page)

    # Click the Pay button
    pay_btn = page.locator(
        ".o_statusbar_buttons button:has-text('Pay'):visible"
    )
    pay_btn.first.click(force=True)
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Wait for the Register Payment dialog
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(1000)

    # Set payment date FIRST (may trigger onchange that resets communication)
    modal_set_date(page, "payment_date", PAYMENT_DATE)
    page.wait_for_timeout(800)

    # Fill Memo LAST — Playwright fill() bypasses pointer-event interception (unlike click())
    modal = page.locator(".modal:visible").last
    comm_inp = modal.locator(".o_field_widget[name='communication'] input").first
    comm_inp.fill(MEMO)
    page.wait_for_timeout(300)

    # Create the payment (direct button click without prior Tab)
    modal_click_button(page, "Create Payment")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
