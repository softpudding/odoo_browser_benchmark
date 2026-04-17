"""Oracle for account.partial_pay_vendor_bill_with_memo."""

from benchmark.oracle_helpers import (
    click_list_row,
    ensure_list_view,
    login,
    modal_click_button,
    modal_set_date,
    navigate,
    run_oracle,
    _dismiss_tooltips,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/vendor-bills")
    _wait_no_loading(page)

    ensure_list_view(page)
    page.wait_for_timeout(600)
    click_list_row(page, "VB-PARTIAL-01")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    _dismiss_tooltips(page)
    page.locator(".o_statusbar_buttons button:has-text('Pay'):visible").first.click(
        force=True
    )
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    page.wait_for_selector(".modal:visible", timeout=10000)

    modal = page.locator(".modal:visible").last
    amount_input = modal.locator(".o_field_widget[name='amount'] input").first
    amount_input.click()
    amount_input.fill("600.00")
    page.wait_for_timeout(300)

    modal_set_date(page, "payment_date", "06/12/2026")
    page.wait_for_timeout(300)

    memo_input = modal.locator(".o_field_widget[name='communication'] input").first
    memo_input.fill("PARTIAL-JUN-600")
    page.wait_for_timeout(300)

    modal_click_button(page, "Create Payment")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
