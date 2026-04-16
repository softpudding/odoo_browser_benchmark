"""Oracle for sale.add_discount_line.

Open draft quotation BENCH-DISC-01, set Discount to 10% on the Desk Organizer
line, and click Save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    set_o2m_field,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the draft quotation
    click_list_row(page, "BENCH-DISC-01")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Set Discount to 10% on the Desk Organizer line (first line)
    set_o2m_field(page, 0, "discount", "10")

    # Click Save
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
