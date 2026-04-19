"""Oracle for purchase_stock.receive_partial_scrap_damaged_units.

Pure Playwright UI oracle:

  1. Navigate to /odoo/purchase and open PO with origin BENCH-SCRAP-RCV-01.
  2. Click the Receive statusbar button to open the incoming transfer.
  3. Open the cog / Actions menu on the receipt and click 'Scrap'.
  4. In the Scrap Products dialog, fill in Product='Bench Widget',
     Quantity=2, Scrap Reason tag='Damaged' and click 'Scrap'.
  5. Back on the receipt, set the Bench Widget move line Done qty to 8
     and click Validate.
  6. In the backorder dialog, click 'No Backorder'.
"""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


PRODUCT_NAME = "Bench Widget"
PO_ORIGIN = "BENCH-SCRAP-RCV-01"
REASON_TAG = "Damaged"


def _set_done_qty(page, row_index, value):
    """Set the Done quantity on a stock move line row inside a picking form."""
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row, "
        ".o_list_view .o_data_row"
    ).nth(row_index)
    cell = row.locator("td[name='quantity'], .o_field_widget[name='quantity']").first
    cell.click()
    page.wait_for_timeout(300)
    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    # ---- 1. Open the PO by origin -------------------------------------
    click_list_row(page, PO_ORIGIN)
    page.wait_for_timeout(1000)

    # ---- 2. Click Receive to open the incoming transfer ---------------
    receive_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Receive'), "
        "button[name='action_view_picking']:visible"
    ).first
    receive_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # ---- 3. Open the cog / Actions menu and click 'Scrap' -------------
    cog = page.locator(
        ".o_cp_action_menus button:visible, "
        ".o_control_panel button.dropdown-toggle:has-text('Actions'):visible, "
        ".o_control_panel .fa-cog:visible"
    ).first
    cog.click()
    page.wait_for_timeout(500)

    scrap_item = page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Scrap'), "
        ".o-dropdown--menu:visible .dropdown-item:has-text('Scrap')"
    ).first
    scrap_item.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # ---- 4. Fill the Scrap Products dialog ----------------------------
    modal = page.locator(".modal:visible").last
    modal.wait_for(state="visible", timeout=10000)

    # Product: Bench Widget (may already be pre-filled from the picking).
    prod_widget = modal.locator(".o_field_widget[name='product_id']").first
    prod_input = prod_widget.locator("input").first
    current_val = (prod_input.input_value() or "").strip()
    if current_val != PRODUCT_NAME:
        prod_input.click()
        prod_input.fill("")
        prod_input.fill(PRODUCT_NAME)
        page.wait_for_timeout(800)
        item = page.locator(
            ".dropdown-menu:visible .dropdown-item, "
            ".ui-autocomplete .ui-menu-item, "
            ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item"
        ).filter(has_text=PRODUCT_NAME).first
        item.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    # Quantity: 2
    qty_input = modal.locator(".o_field_widget[name='scrap_qty'] input").first
    qty_input.click()
    qty_input.fill("")
    qty_input.fill("2")
    qty_input.press("Tab")
    page.wait_for_timeout(300)

    # Reason tag: Damaged (existing tag, select from dropdown)
    tag_input = modal.locator(
        ".o_field_widget[name='scrap_reason_tag_ids'] input"
    ).first
    tag_input.click()
    tag_input.fill(REASON_TAG)
    page.wait_for_timeout(800)
    tag_item = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete .ui-menu-item"
    ).filter(has_text=REASON_TAG).first
    tag_item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Validate the scrap via the dialog's primary action button.
    validate_btn = modal.locator(
        "button[name='action_validate']:visible, "
        ".modal-footer button.btn-primary:has-text('Scrap Products'):visible, "
        ".modal-footer button.btn-primary:has-text('Scrap'):visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    validate_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Handle a potential 'insufficient quantity' warning wizard.
    # The stock.warn.insufficient.qty.scrap wizard's 'Confirm' button is
    # btn-secondary (while 'Discard' is btn-primary), so we must click the
    # button by name/text rather than by primary-style.
    for _ in range(2):
        extra = page.locator(".modal:visible")
        if extra.count() == 0:
            break
        confirm_btn = extra.last.locator(
            "button[name='action_done']:visible, "
            ".modal-footer button:visible:has-text('Confirm')"
        )
        if confirm_btn.count() == 0:
            break
        try:
            confirm_btn.first.click()
        except Exception:
            break
        page.wait_for_timeout(1500)
        _wait_no_loading(page)

    # ---- 5. Back on the receipt: set the Bench Widget qty to 8 -------
    page.wait_for_timeout(500)
    _wait_for_ready(page)
    _set_done_qty(page, 0, "8")
    page.wait_for_timeout(500)

    # ---- 6. Validate the receipt -------------------------------------
    click_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # ---- 7. In the backorder dialog, choose 'No Backorder' -----------
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('No Backorder')").first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
