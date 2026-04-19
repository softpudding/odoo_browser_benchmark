"""Oracle for inventory.cycle_count_two_locations_apply_selected_delta."""

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    clear_search_filters,
    login,
    navigate,
    run_oracle,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/physical-inventory")
    _wait_no_loading(page)
    _wait_for_ready(page)

    clear_search_filters(page)
    searchbox = page.locator(".o_searchview_input").first
    searchbox.click()
    searchbox.fill("Bench Cycle Count Rotor")
    page.wait_for_timeout(500)
    searchbox.press("Enter")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    rows = page.locator(".o_data_row").filter(has_text="Bench Cycle Count Rotor")
    row = None
    for i in range(rows.count()):
        candidate = rows.nth(i)
        qty_cell = candidate.locator("td[name='quantity']").first
        if qty_cell.count() > 0 and qty_cell.inner_text().strip() == "10.00":
            row = candidate
            break
    if row is None:
        raise RuntimeError("target WH/Stock quant row not found")

    qty_cell = row.locator("[name='inventory_quantity'], [name='inventory_quantity_auto_apply']").first
    qty_cell.click()
    page.wait_for_timeout(300)

    qty_input = row.locator(
        "[name='inventory_quantity'] input, [name='inventory_quantity_auto_apply'] input"
    ).first
    qty_input.click(force=True)
    qty_input.press("Control+a")
    qty_input.press("Backspace")
    qty_input.fill("12")
    searchbox.click(force=True)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    rows = page.locator(".o_data_row").filter(has_text="Bench Cycle Count Rotor")
    row = None
    for i in range(rows.count()):
        candidate = rows.nth(i)
        qty_cell = candidate.locator("td[name='quantity']").first
        if qty_cell.count() > 0 and qty_cell.inner_text().strip() == "10.00":
            row = candidate
            break
    if row is None:
        raise RuntimeError("target WH/Stock quant row not found after committing count")

    apply_btn = row.locator(
        "button[name='action_apply_inventory'], "
        "button:has-text('Apply'), "
        ".btn:has-text('Apply')"
    ).first
    apply_btn.click(force=True)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    dialog_btn = page.locator(
        ".modal:visible button[name='action_apply']:visible, "
        ".modal:visible button:has-text('Update Quantities'):visible, "
        ".modal:visible button:has-text('Apply'):visible, "
        ".modal:visible button.btn-primary:visible"
    )
    if dialog_btn.count() > 0:
        dialog_btn.first.click()
        page.wait_for_timeout(1200)
        _wait_no_loading(page)


run_oracle(oracle)
