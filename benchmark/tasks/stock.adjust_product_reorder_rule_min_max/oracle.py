"""Oracle for stock.adjust_product_reorder_rule_min_max.

Flow:
  1. Navigate to /odoo/inventory, open Products > Products.
  2. Search for 'Bench Reorder Item' and click into the product form.
  3. Click the Reordering Rules smart button (label: '0 Reordering Rules'
     before the task; the onclick hits `action_view_orderpoints`).
  4. Land on the Reordering Rules editable-list view (the action strips
     `search_default_trigger` so the list loads unfiltered; product is
     pre-filled via `default_product_id` + `search_default_product_id`).
  5. Click New to open a fresh inline row — Product and Location are
     pre-filled (Bench Reorder Item at WH/Stock) by the action context.
  6. Edit the `product_min_qty` cell, set it to 5.00.
  7. Edit the `product_max_qty` cell, set it to 20.00.
  8. Save the list (breadcrumb Save or list-save button).

UI quirks:
  * The smart button in Odoo 19 renders as a <button> with class
    `oe_stat_button` containing a <field name="nbr_reordering_rules"
    widget="statinfo"/>. We locate it by the button name attribute
    `action_view_orderpoints` OR by visible text 'Reordering Rules'.
  * The editable list's `product_min_qty` column has `string="Min"` and
    `product_max_qty` has `string="Max"` — both are optional=show, so
    they're visible by default (no need to toggle optional columns).
  * After clicking New, Odoo focuses the first editable cell (which is
    `product_id`); we must Tab or click into the Min column before
    editing — safer to click the specific cell by `[name='...']`.
  * Save affordance: the breadcrumb save button is `.o_form_button_save`
    when in a form; for the list it's `.o_list_button_save` or the
    breadcrumb Save button. We try both.
"""

from benchmark.oracle_helpers import (
    click_create,
    full_url,
    login,
    navigate,
    run_oracle,
    save_form,
    search_for,
    _wait_no_loading,
    _wait_for_ready,
)

PRODUCT_NAME = "Bench Reorder Item"
MIN_QTY = "5"
MAX_QTY = "20"


def _open_products_list(page):
    # Navigate to the Products list (action=stock.product_template_action_product).
    # Fall back to the Inventory > Products > Products menu if the direct
    # URL doesn't resolve.
    page.goto(
        full_url("/odoo/action-stock.product_template_action_product"),
        timeout=60000,
    )
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


def _open_product(page, name):
    search_for(page, name)
    page.wait_for_timeout(600)
    _wait_no_loading(page)
    # Click the first matching card/row.
    rec = page.locator(
        f".o_kanban_record:has-text('{name}'), "
        f".o_list_view .o_data_row:has-text('{name}')"
    ).first
    rec.wait_for(state="visible", timeout=10000)
    rec.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


def _click_reordering_smart_button(page):
    # Primary: a <button> whose name attribute is action_view_orderpoints
    # and whose visible text includes 'Reordering Rules'.
    btn = page.locator(
        "button[name='action_view_orderpoints']:visible"
    ).filter(has_text="Reordering Rules").first
    if btn.count() == 0:
        btn = page.locator(
            "button[name='action_view_orderpoints']:visible"
        ).first
    btn.wait_for(state="visible", timeout=10000)
    btn.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def _click_new_inline_row(page):
    # Prefer the list's dedicated New button (`o_list_button_add`); fall
    # back to the generic helper.
    btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    if btn.count() > 0:
        btn.click()
    else:
        click_create(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


def _set_numeric_cell(page, field_name, value):
    # Target the currently-selected row's cell for the given field.
    row = page.locator(".o_list_view .o_data_row.o_selected_row").first
    if row.count() == 0:
        row = page.locator(".o_list_view .o_data_row").first
    cell = row.locator(f"[name='{field_name}']").first
    cell.wait_for(state="visible", timeout=10000)
    cell.click()
    page.wait_for_timeout(300)

    inp = row.locator(f"[name='{field_name}'] input").first
    if inp.count() == 0 or not inp.is_visible():
        # Double-click to enter edit mode if needed.
        cell.dblclick()
        page.wait_for_timeout(300)
        inp = row.locator(f"[name='{field_name}'] input").first
    inp.click(click_count=3)
    inp.fill("")
    inp.type(str(value))
    inp.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def _save_list(page):
    # Try the list-specific save button first.
    save_btn = page.locator(
        ".o_list_button_save:visible, "
        ".o_form_button_save:visible, "
        ".o_control_panel button:has-text('Save'):visible"
    ).first
    if save_btn.count() > 0:
        save_btn.click()
        page.wait_for_timeout(800)
        _wait_no_loading(page)
    else:
        save_form(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)

    _open_products_list(page)
    _open_product(page, PRODUCT_NAME)
    _click_reordering_smart_button(page)
    _click_new_inline_row(page)

    _set_numeric_cell(page, "product_min_qty", MIN_QTY)
    _set_numeric_cell(page, "product_max_qty", MAX_QTY)

    _save_list(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
