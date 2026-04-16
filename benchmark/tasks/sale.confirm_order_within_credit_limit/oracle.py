"""Oracle for sale.confirm_order_within_credit_limit.

Open the Atlas Field Systems quotation, reduce Field Router Kit from 4 to 3,
and confirm the order.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    click_status_button,
    login,
    navigate,
    set_o2m_field,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    clear_search_filters(page)
    page.wait_for_timeout(500)

    click_list_row(page, "Atlas Field Systems")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    set_o2m_field(page, 0, "product_uom_qty", "3")
    page.wait_for_timeout(500)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
