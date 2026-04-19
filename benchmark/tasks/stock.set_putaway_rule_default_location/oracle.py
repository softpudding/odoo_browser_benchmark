"""Oracle for stock.set_putaway_rule_default_location.

Navigate to Inventory > Configuration > Putaway Rules via the action
xmlid `stock.action_putaway_tree` (the same path the UI Configuration
menu link ultimately resolves to). Click New to add an inline row,
then fill three many2one fields inline:
  - When product arrives in (location_in_id) = "WH/Stock"
  - Product (product_id)                     = "Bench Putaway Item"
  - Store to (location_out_id)               = "WH/Stock/Shelf B"
Then save the list.

Leave category_id empty (this is a product-level putaway rule).
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


PRODUCT_NAME = "Bench Putaway Item"
LOCATION_IN = "WH/Stock"
LOCATION_OUT = "WH/Stock/Shelf B"
SHELF_NAME = "Shelf B"


def _fill_inline_m2o(page, field_name, search_text, exact_text):
    """Fill a many2one cell inside the currently-selected inline row."""
    row = page.locator(".o_data_row.o_selected_row").first
    cell = row.locator(
        f"td[name='{field_name}'], .o_field_widget[name='{field_name}']"
    ).first
    cell.click()
    page.wait_for_timeout(300)

    inp = cell.locator("input").first
    inp.click()
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(1000)

    dropdown_items = page.locator(
        ".dropdown-menu .dropdown-item:visible, "
        ".o-autocomplete--dropdown-item:visible"
    )
    matched = None
    n = dropdown_items.count()
    for i in range(n):
        item = dropdown_items.nth(i)
        text = item.inner_text().strip()
        if text == exact_text:
            matched = item
            break
    if matched is None:
        for i in range(n):
            item = dropdown_items.nth(i)
            text = item.inner_text().strip()
            if text.startswith(exact_text):
                matched = item
                break
    if matched is None:
        for i in range(n):
            item = dropdown_items.nth(i)
            text = item.inner_text().strip()
            if search_text in text and "Search" not in text and "Create" not in text:
                matched = item
                break
    if matched is None:
        raise RuntimeError(
            f"No dropdown match for field={field_name} search={search_text!r} "
            f"exact={exact_text!r}"
        )
    matched.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-stock.action_putaway_tree")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Click "New" to add a new inline row at the bottom.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Ensure a selected row is visible.
    page.wait_for_selector(".o_data_row.o_selected_row", timeout=10000)

    # 1. When product arrives in (location_in_id) — source location.
    _fill_inline_m2o(page, "location_in_id", "WH/Stock", LOCATION_IN)

    # 2. Product (product_id) — the product the rule applies to.
    _fill_inline_m2o(page, "product_id", PRODUCT_NAME, PRODUCT_NAME)

    # 3. Store to (location_out_id) — destination sublocation.
    _fill_inline_m2o(page, "location_out_id", SHELF_NAME, LOCATION_OUT)

    # Save the list view (commit the pending row).
    save_btn = page.locator(
        ".o_list_button_save:visible, "
        ".o_list_record_save:visible, "
        ".o_form_button_save:visible, "
        ".o_control_panel button[name='save']:visible, "
        ".o_control_panel_main_buttons button:has-text('Save'):visible"
    )
    if save_btn.count() > 0:
        save_btn.first.click()
        page.wait_for_timeout(800)
    else:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
    _wait_no_loading(page)
    page.wait_for_timeout(800)


run_oracle(oracle)
