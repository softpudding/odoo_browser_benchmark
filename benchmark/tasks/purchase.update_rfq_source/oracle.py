"""Oracle for purchase.update_rfq_source."""

from benchmark.oracle_helpers import (
    click_tab,
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
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "BENCH-SRC-01")
    _wait_for_ready(page)

    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "origin", "BENCH-SRC-01-UPDATED")
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
