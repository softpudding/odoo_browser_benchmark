"""Oracle for purchase_stock.receive_partial_scrap_damaged_units.

Part A: open the PO, click the Receipt smart button.
Part B: set Done=15 on the Bench Parts move row.
Part C: cog Actions > Scrap, fill product=Bench Parts, qty=5,
        scrap_location_id=WH/Lost, then click Scrap Products.
Part D: click Validate, then Create Backorder on the dialog.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_stat_button,
    click_status_button,
    full_url,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)

PO_ORIGIN = "P-BENCH-DMG-001"
PRODUCT_NAME = "Bench Parts"
LOST_LOC = "WH/Lost"


def _set_done_qty(page, row_index, value):
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row, "
        ".o_list_view .o_data_row"
    ).nth(row_index)
    cell = row.locator(
        "td[name='quantity'], .o_field_widget[name='quantity']"
    ).first
    cell.click()
    page.wait_for_timeout(300)
    inp = cell.locator("input").first
    if inp.count() == 0:
        inp = row.locator("input:visible").first
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _open_po_and_receipt(page):
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_list_row(page, PO_ORIGIN)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Click the Receipt smart button. In Odoo 19, the header smart button
    # for receipts is "Receive" / "Receipt".
    receipt_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Receive'), "
        ".oe_stat_button:visible:has-text('Receipt'), "
        "button[name='action_view_picking']:visible"
    ).first
    receipt_btn.wait_for(state="visible", timeout=15000)
    receipt_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)


def _set_done_15(page):
    # There is exactly one move line for Bench Parts in the picking form.
    _set_done_qty(page, 0, "15")

    # Persist by clicking the save button if form is dirty.
    save_btn = page.locator(".o_form_button_save:visible")
    if save_btn.count() > 0:
        try:
            save_btn.first.click()
            page.wait_for_timeout(700)
            _wait_no_loading(page)
        except Exception:
            pass


def _open_cog_scrap(page):
    # Open the cog / Actions menu on the control panel.
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
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def _fill_scrap_dialog(page):
    modal = page.locator(".modal:visible").last
    modal.wait_for(state="visible", timeout=10000)

    # Product: Bench Parts.
    prod_input = modal.locator(
        ".o_field_widget[name='product_id'] input"
    ).first
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

    # Quantity: overwrite default 1 with 5.
    qty_input = modal.locator(
        ".o_field_widget[name='scrap_qty'] input"
    ).first
    qty_input.click()
    qty_input.fill("")
    qty_input.fill("5")
    qty_input.press("Tab")
    page.wait_for_timeout(400)

    # Scrap Location: change from Virtual Locations/Scrap to WH/Lost.
    scrap_loc_input = modal.locator(
        ".o_field_widget[name='scrap_location_id'] input"
    ).first
    scrap_loc_input.click()
    scrap_loc_input.fill("")
    scrap_loc_input.fill(LOST_LOC)
    page.wait_for_timeout(900)
    loc_item = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete .ui-menu-item"
    ).filter(has_text=LOST_LOC).first
    try:
        loc_item.click()
    except Exception:
        scrap_loc_input.press("Enter")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Validate scrap.
    validate_btn = modal.locator(
        "button[name='action_validate']:visible, "
        ".modal-footer button.btn-primary:has-text('Scrap Products'):visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    validate_btn.click()
    page.wait_for_timeout(1800)
    _wait_no_loading(page)

    # A secondary insufficient-qty wizard should NOT appear because the
    # product is consumable (is_storable=False). But guard anyway.
    for _ in range(2):
        extra = page.locator(".modal:visible")
        if extra.count() == 0:
            break
        pbtn = extra.last.locator("button.btn-primary:visible").first
        if pbtn.count() == 0:
            break
        try:
            pbtn.click()
        except Exception:
            break
        page.wait_for_timeout(1200)
        _wait_no_loading(page)


def _validate_and_backorder(page):
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    click_status_button(page, "Validate")
    page.wait_for_timeout(1800)
    _wait_no_loading(page)

    # Backorder dialog — click Create Backorder (primary).
    for _ in range(3):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        m = modal.last
        cb = m.locator("button:has-text('Create Backorder'):visible")
        if cb.count() > 0:
            cb.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
            continue
        # If any other confirmation modal appears, accept primary.
        pbtn = m.locator("button.btn-primary:visible").first
        if pbtn.count() > 0:
            pbtn.click()
            page.wait_for_timeout(1200)
            _wait_no_loading(page)
        else:
            break


def oracle(page):
    login(page)

    _open_po_and_receipt(page)
    _set_done_15(page)
    _open_cog_scrap(page)
    _fill_scrap_dialog(page)
    _validate_and_backorder(page)


run_oracle(oracle)
