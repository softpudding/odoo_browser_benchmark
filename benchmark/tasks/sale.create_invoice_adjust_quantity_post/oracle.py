"""Oracle for sale.create_invoice_adjust_quantity_post."""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    set_date,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, "MED-INV-SO-01")
    page.wait_for_timeout(800)

    click_button(page, "Create Invoice")
    page.wait_for_timeout(1000)

    if page.locator(".modal:visible").count() > 0:
        create_btn = page.locator(
            ".modal:visible button[name='create_invoices'], "
            ".modal:visible button:has-text('Create Draft')"
        )
        create_btn.first.click()
        page.wait_for_timeout(1200)
        _wait_no_loading(page)

    set_date(page, "invoice_date", "05/12/2026")
    page.wait_for_timeout(400)
    set_many2one(page, "invoice_payment_term_id", "30 Net Days")
    page.wait_for_timeout(400)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
