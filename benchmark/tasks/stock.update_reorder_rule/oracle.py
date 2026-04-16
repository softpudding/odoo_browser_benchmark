"""Oracle for stock.update_reorder_rule.

Navigate to Inventory > Replenishment (Reordering Rules view), find the rule
for 'Steel Bracket 12"', update Min Qty to 50 and Max Qty to 200, then save.

In Odoo 19, the Reordering Rules list is at /odoo/action-641.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)

TARGET_PRODUCT = 'Steel Bracket 12"'
NEW_MIN = "50"
NEW_MAX = "200"


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-641")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Search for the target product to find its row
    search_input = page.locator(".o_searchview_input").first
    search_input.fill(TARGET_PRODUCT)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Find the row for the target product
    row = page.locator(f".o_data_row:has-text('{TARGET_PRODUCT}')").first
    row.wait_for(state="visible", timeout=10000)

    # Click the Min Quantity cell to edit it
    min_cell = row.locator("[name='product_min_qty']").first
    min_cell.click()
    page.wait_for_timeout(300)
    min_input = page.locator(".o_selected_row [name='product_min_qty'] input, "
                              ".o_data_row.o_selected_row [name='product_min_qty'] input").first
    if min_input.count() == 0:
        min_input = min_cell.locator("input").first
    min_input.click(click_count=3)
    min_input.fill(NEW_MIN)
    page.wait_for_timeout(200)

    # Click the Max Quantity cell
    max_cell = row.locator("[name='product_max_qty']").first
    max_cell.click()
    page.wait_for_timeout(300)
    max_input = page.locator(".o_selected_row [name='product_max_qty'] input, "
                              ".o_data_row.o_selected_row [name='product_max_qty'] input").first
    if max_input.count() == 0:
        max_input = max_cell.locator("input").first
    max_input.click(click_count=3)
    max_input.fill(NEW_MAX)
    page.wait_for_timeout(200)

    # Save the list view changes
    save_btn = page.locator(
        ".o_list_button_save:visible, "
        ".o_list_record_save:visible, "
        ".o_form_button_save:visible, "
        ".o_control_panel button[name='save']:visible"
    ).first
    if save_btn.count() > 0:
        save_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
