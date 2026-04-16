"""Oracle for account.register_payment_defaults.

Open posted invoice BENCH-PAY-01 for Lakeview Partners, click Pay button,
accept all defaults in the Register Payment wizard, and click Create Payment.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    modal_click_button,
    ensure_list_view,
    _dismiss_tooltips,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    ensure_list_view(page)
    click_list_row(page, "Lakeview Partners")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    _dismiss_tooltips(page)
    pay_btn = page.locator(
        ".o_statusbar_buttons button:has-text('Pay'):visible"
    )
    pay_btn.first.click(force=True)
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(1000)

    modal_click_button(page, "Create Payment")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
