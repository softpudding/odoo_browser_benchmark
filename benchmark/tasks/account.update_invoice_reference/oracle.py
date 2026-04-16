"""Oracle for account.update_invoice_reference."""

from benchmark.oracle_helpers import (
    ensure_list_view,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
    click_list_row,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    ensure_list_view(page)
    click_list_row(page, "BENCH-INV-REF-01")
    _wait_for_ready(page)

    fill_field(page, "ref", "BENCH-INV-REF-01-UPDATED")
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
