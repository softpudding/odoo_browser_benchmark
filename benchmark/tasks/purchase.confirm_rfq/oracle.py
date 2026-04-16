"""Oracle for purchase.confirm_rfq."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "BENCH-CONFIRM-01")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
