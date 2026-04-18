"""Oracle for purchase_stock.return_partial_with_distractor_lines.

Open PO P-BENCH-RET-001, launch the Return wizard from the completed receipt,
explicitly set return qty=0 on the two distractor rows (WidgetA, WidgetC) and
qty=2 on WidgetB, create the return, and validate it.
"""

from benchmark.oracle_helpers import (
    click_button_name,
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def _set_return_qty_for_product(page, product_name, value):
    """Find the return-wizard row whose product cell contains product_name and
    set its quantity cell to value."""
    rows = page.locator(".modal:visible .o_list_renderer .o_data_row")
    n = rows.count()
    for i in range(n):
        row = rows.nth(i)
        if product_name in row.inner_text():
            cell = row.locator("td[name='quantity'], .o_field_widget[name='quantity']").first
            cell.click()
            page.wait_for_timeout(300)
            inp = cell.locator("input").first
            inp.fill("")
            inp.fill(value)
            inp.press("Tab")
            page.wait_for_timeout(500)
            _wait_no_loading(page)
            return
    raise AssertionError(f"Could not find return wizard row for {product_name!r}")


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "P-BENCH-RET-001")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_button_name(page, "action_view_picking")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    page.get_by_role("button", name="Return", exact=True).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    page.wait_for_selector(".modal:visible .o_list_renderer .o_data_row", timeout=30000)

    # Explicitly zero out the distractor rows and set WidgetB to 2
    _set_return_qty_for_product(page, "Bayside WidgetA", "0")
    _set_return_qty_for_product(page, "Bayside WidgetC", "0")
    _set_return_qty_for_product(page, "Bayside WidgetB", "2")

    page.locator(".modal:visible button[name='action_create_returns']").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    page.get_by_role("button", name="Validate", exact=True).first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Handle a possible backorder/confirmation modal
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        no_bo = modal.last.locator("button:has-text('No Backorder')")
        if no_bo.count() > 0:
            no_bo.first.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)


run_oracle(oracle)
