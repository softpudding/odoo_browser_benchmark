"""Oracle for stock.adjust_inventory_with_location_filter."""

from benchmark.oracle_helpers import login, navigate, run_oracle, _wait_no_loading


def oracle(page):
    login(page)
    navigate(page, "/odoo/physical-inventory")
    _wait_no_loading(page)

    search = page.locator(".o_searchview_input").first
    search.click()
    search.fill("WH/Stock")
    page.wait_for_timeout(800)
    items = page.locator(".o_searchview_autocomplete:visible .o-dropdown-item, .o_searchview_autocomplete:visible .o_menu_item")
    items.nth(1).click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    search = page.locator(".o_searchview_input").first
    search.click()
    search.fill("Servo Motor A1")
    page.wait_for_timeout(800)
    items = page.locator(".o_searchview_autocomplete:visible .o-dropdown-item, .o_searchview_autocomplete:visible .o_menu_item")
    items.nth(0).click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    row = page.locator(".o_data_row").filter(has_text="Servo Motor A1").first
    row.wait_for(state="visible", timeout=10000)
    qty_cell = row.locator("[name='inventory_quantity']").first
    qty_cell.click()
    page.wait_for_timeout(400)
    qty_input = row.locator("[name='inventory_quantity'] input").first
    qty_input.fill("18")
    qty_input.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    page.get_by_role("button", name="Save").first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    discard = page.get_by_role("button", name="Discard")
    if discard.count() > 0:
        discard.first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    row = page.locator(".o_data_row").filter(has_text="Servo Motor A1").first
    row.locator("button[name='action_apply_inventory']").first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
