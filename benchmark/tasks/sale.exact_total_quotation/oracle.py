"""Oracle for sale.exact_total_quotation.

Find draft quotation for Deco Addict. Fix the prices to achieve
total 1330: Standing Desk 400, Office Chair 175, Whiteboard 90.
Expected: 2*400 + 3*175 + 1*90 = 1330.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    save_form,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the Deco Addict quotation
    click_list_row(page, "Deco Addict")
    page.wait_for_timeout(1000)

    # Fix Standing Desk price: 450 -> 400 (row 0)
    set_o2m_field(page, 0, "price_unit", "400")
    page.wait_for_timeout(500)

    # Fix Office Chair price: 150 -> 175 (row 1)
    set_o2m_field(page, 1, "price_unit", "175")
    page.wait_for_timeout(500)

    # Fix Whiteboard price: 80 -> 90 (row 2)
    set_o2m_field(page, 2, "price_unit", "90")
    page.wait_for_timeout(500)

    # Save
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
