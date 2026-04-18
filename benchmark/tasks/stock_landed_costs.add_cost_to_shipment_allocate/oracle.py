"""Oracle for stock_landed_costs.add_cost_to_shipment_allocate.

Flow:
  Part A: open /odoo/landed-costs, click New.
  Part B: pick receipt R-BENCH-LC-001 in the picking_ids many2many_tags
          autocomplete.
  Part C: add one cost line — product Freight, confirm split_method =
          'By Quantity', cost = 45.
  Part D: click Compute (under the cost_lines list), then the header
          Validate button.
"""

from benchmark.oracle_helpers import (
    full_url,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)

RECEIPT_REF = "R-BENCH-LC-001"
PRODUCT_NAME = "Freight"
COST_VALUE = "45"


def _open_landed_cost_new(page):
    navigate(page, "/odoo/landed-costs")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Click New / Create button
    new_btn = page.locator(
        ".o_control_panel_main_buttons button:visible:has-text('New'), "
        "button.o_list_button_add:visible, "
        ".o_cp_buttons button.o_list_button_add:visible"
    ).first
    new_btn.wait_for(state="visible", timeout=10000)
    new_btn.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)


def _pick_transfer(page):
    widget = page.locator(
        ".o_field_widget[name='picking_ids']"
    ).first
    widget.wait_for(state="visible", timeout=10000)

    # Many2many_tags: click the input box, type, pick autocomplete item.
    inp = widget.locator("input").first
    inp.click()
    page.wait_for_timeout(200)
    inp.fill(RECEIPT_REF)
    page.wait_for_timeout(900)
    item = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete .ui-menu-item"
    ).filter(has_text=RECEIPT_REF).first
    try:
        item.wait_for(state="visible", timeout=5000)
        item.click()
    except Exception:
        inp.press("Enter")
    page.wait_for_timeout(600)
    _wait_no_loading(page)


def _add_cost_line(page):
    # Cost Lines editable list: click "Add a line"
    add_line = page.locator(
        ".o_field_widget[name='cost_lines'] .o_field_x2many_list_row_add a, "
        ".o_field_widget[name='cost_lines'] a:has-text('Add a line'):visible"
    ).first
    add_line.wait_for(state="visible", timeout=8000)
    add_line.click()
    page.wait_for_timeout(500)

    # Product autocomplete in the newly-added row.
    row = page.locator(
        ".o_field_widget[name='cost_lines'] .o_data_row.o_selected_row"
    ).first
    row.wait_for(state="visible", timeout=8000)

    prod_cell = row.locator(
        "td[name='product_id'], .o_field_widget[name='product_id']"
    ).first
    prod_cell.click()
    page.wait_for_timeout(200)
    prod_input = row.locator(
        ".o_field_widget[name='product_id'] input"
    ).first
    prod_input.click()
    prod_input.fill("")
    prod_input.fill(PRODUCT_NAME)
    page.wait_for_timeout(900)
    item = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete .ui-menu-item"
    ).filter(has_text=PRODUCT_NAME).first
    item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Verify split_method is 'By Quantity' (set by product onchange);
    # leave it as-is.

    # Cost = 45 (overwrite whatever the product's standard_price filled).
    price_cell = row.locator(
        "td[name='price_unit'], .o_field_widget[name='price_unit']"
    ).first
    price_cell.click()
    page.wait_for_timeout(200)
    price_inp = row.locator(
        ".o_field_widget[name='price_unit'] input"
    ).first
    price_inp.fill("")
    price_inp.fill(COST_VALUE)
    price_inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _click_compute(page):
    # Compute button lives inside the Additional Costs tab, below the
    # cost_lines list, inside the subtotal group. Its name attribute
    # is 'compute_landed_cost'.
    compute_btn = page.locator(
        "button[name='compute_landed_cost']:visible, "
        ".o_form_view button:has-text('Compute'):visible"
    ).first
    compute_btn.wait_for(state="visible", timeout=10000)
    compute_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def _click_validate(page):
    # First, save the form if it's dirty — the Validate button is only
    # effective on a saved record.
    save_btn = page.locator(".o_form_button_save:visible")
    if save_btn.count() > 0:
        try:
            save_btn.first.click()
            page.wait_for_timeout(700)
            _wait_no_loading(page)
        except Exception:
            pass

    validate_btn = page.locator(
        ".o_statusbar_buttons button[name='button_validate']:visible"
    ).first
    try:
        validate_btn.wait_for(state="visible", timeout=10000)
    except Exception:
        validate_btn = page.locator(
            ".o_statusbar_buttons button:visible:has-text('Validate')"
        ).first
        validate_btn.wait_for(state="visible", timeout=10000)
    validate_btn.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    _open_landed_cost_new(page)
    _pick_transfer(page)
    _add_cost_line(page)
    _click_compute(page)
    _click_validate(page)


run_oracle(oracle)
