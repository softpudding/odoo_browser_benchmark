"""Oracle for inventory.create_storage_category_assign_to_location.

Steps:
  1. Navigate to Inventory Settings (action stock.action_stock_config_settings)
     and toggle on the 'Storage Locations' setting (group_stock_multi_locations).
     Save the settings — this exposes the Storage Categories menu and the
     storage_category_id field on stock.location.
  2. Navigate to Storage Categories list (stock.action_storage_category),
     click New, fill name='Cold Chain' and max_weight=500, save.
  3. Navigate to Locations list (stock.action_location_form), open WH/Stock,
     set storage_category_id='Cold Chain', save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


CATEGORY_NAME = "Cold Chain"


def _enable_storage_locations(page):
    navigate(page, "/odoo/action-stock.action_stock_config_settings")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # The setting is group_stock_multi_locations. The widget is a checkbox
    # inside the .o_field_widget[name='group_stock_multi_locations'].
    field = page.locator(
        ".o_field_widget[name='group_stock_multi_locations']"
    ).first
    field.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    cb = field.locator("input[type='checkbox']").first
    if not cb.is_checked():
        cb.click()
        page.wait_for_timeout(400)

    # Save the settings (button in the control panel)
    save_btn = page.locator(
        ".o_control_panel button[name='execute']:visible, "
        ".o_control_panel button:has-text('Save'):visible, "
        "button.o_form_button_save:visible"
    ).first
    save_btn.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)
    page.wait_for_timeout(2000)


def _create_storage_category(page):
    navigate(page, "/odoo/action-stock.action_storage_category")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)
    _wait_for_ready(page)

    # Click New (control panel)
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # The form opens. Fill name.
    name_field = page.locator(
        ".o_field_widget[name='name'] input:visible, "
        ".o_field_widget[name='name'] textarea:visible"
    ).first
    name_field.click()
    name_field.fill(CATEGORY_NAME)
    page.wait_for_timeout(200)

    # Fill max_weight = 500
    weight_field = page.locator(
        ".o_field_widget[name='max_weight'] input:visible"
    ).first
    weight_field.click()
    weight_field.fill("")
    weight_field.fill("500")
    page.wait_for_timeout(200)

    # Save
    save_form(page)
    page.wait_for_timeout(800)


def _assign_to_wh_stock(page):
    navigate(page, "/odoo/action-stock.action_location_form")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)
    _wait_for_ready(page)

    # Find the WH/Stock row by complete_name (column "Location"). The list view
    # uses complete_name in the display. Click directly.
    # Use a specific row that has "WH/Stock" exactly (not WH/Stock/Shelf).
    # The "complete_name" column shows the full path.
    rows = page.locator(".o_data_row")
    n = rows.count()
    target = None
    for i in range(n):
        row = rows.nth(i)
        text = row.inner_text().strip()
        # rows are like "WH\tStock" or "WH/Stock\tInternal Location"
        # We want the row whose complete_name = "WH/Stock" (no further /).
        if "WH/Stock\n" in text or text.startswith("WH/Stock\n"):
            # Heuristic: prefer the shortest text starting with WH/Stock
            target = row
            break
        if "WH/Stock\t" in text and "WH/Stock/" not in text:
            target = row
            break
    if target is None:
        # Fallback: look for any cell whose text equals WH/Stock
        cell = page.locator(".o_data_row td:has-text('WH/Stock')").first
        cell.click()
    else:
        target.locator("td").nth(1).click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Set storage_category_id = Cold Chain
    set_many2one(page, "storage_category_id", CATEGORY_NAME)
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(600)


def oracle(page):
    login(page)
    _enable_storage_locations(page)
    _create_storage_category(page)
    _assign_to_wh_stock(page)


run_oracle(oracle)
