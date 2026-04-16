"""Oracle for account.update_customer_invoice_terms_post."""

from benchmark.oracle_helpers import (
    click_tab,
    click_list_row,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_date,
    set_many2one,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    click_list_row(page, "MED-CINV-01")
    page.wait_for_timeout(1000)

    set_date(page, "invoice_date", "05/14/2026")
    page.wait_for_timeout(400)
    set_many2one(page, "invoice_payment_term_id", "30 Net Days")
    page.wait_for_timeout(400)
    set_o2m_field(page, 0, "quantity", "4")
    page.wait_for_timeout(500)

    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "ref", "BRIGHT-READY")
    page.wait_for_timeout(400)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
