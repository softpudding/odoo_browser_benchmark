"""Oracle for sale.create_invoice_register_payment_memo."""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    click_status_button,
    login,
    modal_click_button,
    modal_set_date,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, "PAYFLOW-01")
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    click_button(page, "Create Invoice")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    if page.locator(".modal:visible").count() > 0:
        create_btn = page.locator(
            ".modal:visible button[name='create_invoices'], "
            ".modal:visible button:has-text('Create Draft')"
        )
        create_btn.first.click()
        page.wait_for_timeout(1200)
        _wait_no_loading(page)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    pay_btn = page.locator(".o_statusbar_buttons button:has-text('Pay'):visible")
    pay_btn.first.click(force=True)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    modal_set_date(page, "payment_date", "05/21/2026")
    page.wait_for_timeout(500)

    modal = page.locator(".modal:visible").last
    memo_input = modal.locator(".o_field_widget[name='communication'] input").first
    memo_input.fill("PAYFLOW-MAY-SETTLEMENT")
    page.wait_for_timeout(300)

    modal_click_button(page, "Create Payment")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
