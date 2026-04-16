"""Oracle for account.update_vendor_bill_reference_post."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/vendor-bills")
    _wait_no_loading(page)

    click_list_row(page, "MED-VB-DRAFT-01")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    set_date(page, "invoice_date", "05/06/2026")
    page.wait_for_timeout(400)
    fill_field(page, "ref", "MSC-8841")
    page.wait_for_timeout(400)
    set_o2m_field(page, 0, "quantity", "60")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(600)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
