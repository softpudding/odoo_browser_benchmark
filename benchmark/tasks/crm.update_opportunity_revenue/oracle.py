"""Oracle for crm.update_opportunity_revenue."""

from benchmark.oracle_helpers import (
    click_list_row,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    click_list_row(page, "BENCH-OPP-REV-01")
    _wait_for_ready(page)

    fill_field(page, "expected_revenue", "12500")
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
