"""Oracle for sale.change_validity_date.

Open draft quotation BENCH-VALID-01 for Lakeview Partners, change the
Expiration date to May 15, 2026, and click Save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    set_date,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the draft quotation BENCH-VALID-01
    click_list_row(page, "BENCH-VALID-01")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Change the Expiration date to May 15, 2026
    set_date(page, "validity_date", "05/15/2026")

    # Click Save
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
