"""Oracle for purchase_stock.return_partial_receipt_to_vendor.

Open PO RET-PO-07, launch the Return wizard from the completed receipt, set
exact quantities, create the return, and validate it.
"""

from benchmark.oracle_helpers import (
    click_button,
    click_button_name,
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def _set_return_qty(page, row_index, value):
    row = page.locator(".modal:visible .o_list_renderer .o_data_row").nth(row_index)
    cell = row.locator("td[name='quantity'], .o_field_widget[name='quantity']").first
    cell.click()
    page.wait_for_timeout(300)
    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "RET-PO-07")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_button_name(page, "action_view_picking")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    page.get_by_role("button", name="Return", exact=True).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    page.wait_for_selector(".modal:visible .o_list_renderer .o_data_row", timeout=30000)

    _set_return_qty(page, 0, "2")
    _set_return_qty(page, 1, "0")
    _set_return_qty(page, 2, "1")

    page.locator(".modal:visible button[name='action_create_returns']").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    page.get_by_role("button", name="Validate", exact=True).first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
