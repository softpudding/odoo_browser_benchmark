"""Oracle for inventory.filtered_cycle_count_apply_single_line."""
from benchmark.oracle_helpers import (
    _wait_no_loading,
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    search_for,
)

def oracle(page):
    login(page)
    navigate(page, "/odoo/action-stock.action_view_inventory_tree")
    ensure_list_view(page)
    clear_search_filters(page)
    search_for(page, "Bench Cycle Rotor")
    row = page.locator(".o_list_view .o_data_row").filter(
        has_text="Bench Cycle Rotor"
    ).filter(has_text="7.00").first
    row.wait_for(timeout=15000)

    qty_cell = row.locator("td[name='inventory_quantity'], .o_data_cell[name='inventory_quantity']").first
    qty_cell.click()
    qty_input = page.locator(
        "input[name='inventory_quantity'], .o_field_widget[name='inventory_quantity'] input"
    ).last
    qty_input.fill("11")
    qty_input.press("Tab")
    _wait_no_loading(page)

    date_cell = row.locator("td[name='inventory_date'], .o_data_cell[name='inventory_date']").first
    date_cell.click()
    date_input = page.locator(
        "input[name='inventory_date'], .o_field_widget[name='inventory_date'] input"
    ).last
    date_input.fill("05/15/2026")
    date_input.press("Tab")
    _wait_no_loading(page)

    row.locator("button[name='action_apply_inventory']").first.click()
    _wait_no_loading(page)

run_oracle(oracle)
