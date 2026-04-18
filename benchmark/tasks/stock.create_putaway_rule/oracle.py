"""Oracle for stock.create_putaway_rule.

Navigate to Inventory > Configuration > Putaway Rules (an editable=bottom
list), click New to add a row, then fill three many2one fields inline:
  - Product = "Storage Box Echo"
  - When product arrives in (location_in_id) = "WH/Stock"
  - Store to (location_out_id) = "WH/Stock/Shelf A1"
Then save the list.

In Odoo 19 the Putaway Rules action is `stock.action_putaway_tree` → id 565.
We navigate to /odoo/action-565 to avoid depending on menu text.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


TARGET_PRODUCT = "Storage Box Echo"
LOCATION_IN = "WH/Stock"
LOCATION_OUT = "WH/Stock/Shelf A1"
SHELF_NAME = "Shelf A1"


def _fill_inline_m2o(page, field_name, search_text, exact_text):
    """Fill a many2one cell inside the currently-selected inline row.

    Looks up the cell by [name=...] inside the selected o_data_row, types
    the search text, waits for the dropdown, and clicks the entry whose
    visible text matches exact_text.
    """
    row = page.locator(".o_data_row.o_selected_row").first
    cell = row.locator(f"td[name='{field_name}'], .o_field_widget[name='{field_name}']").first
    cell.click()
    page.wait_for_timeout(300)

    inp = cell.locator("input").first
    inp.click()
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(1000)

    # Try to click a dropdown item whose visible label is exact_text.
    # We look at any visible dropdown-item and pick the one that matches.
    dropdown_items = page.locator(".dropdown-menu .dropdown-item:visible, .o-autocomplete--dropdown-item:visible")
    matched = None
    n = dropdown_items.count()
    for i in range(n):
        item = dropdown_items.nth(i)
        text = item.inner_text().strip()
        if text == exact_text:
            matched = item
            break
    if matched is None:
        # Fallback: pick the first item that starts with exact_text
        for i in range(n):
            item = dropdown_items.nth(i)
            text = item.inner_text().strip()
            if text.startswith(exact_text):
                matched = item
                break
    if matched is None:
        # Very last fallback: any item that contains the search text
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
    # The Putaway Rules action (stock.action_putaway_tree)
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

    # Ensure a selected row is visible (Odoo 19 inline editable list).
    page.wait_for_selector(".o_data_row.o_selected_row", timeout=10000)

    # 1. When product arrives in (location_in_id) — source location.
    _fill_inline_m2o(page, "location_in_id", "WH/Stock", LOCATION_IN)

    # 2. Product.
    _fill_inline_m2o(page, "product_id", TARGET_PRODUCT, TARGET_PRODUCT)

    # 3. Store to (location_out_id) — destination sublocation.
    # This field only becomes editable once location_in_id is set.
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
        # Fallback: press Escape/Enter on the row to commit, then try save again
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
    _wait_no_loading(page)
    page.wait_for_timeout(800)


run_oracle(oracle)
