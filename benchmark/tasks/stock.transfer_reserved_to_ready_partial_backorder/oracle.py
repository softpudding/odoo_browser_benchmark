"""Oracle for stock.transfer_reserved_to_ready_partial_backorder.

Part A: open delivery D-BENCH-PARTIAL-001, click Check Availability.
Part B: open Detailed Operations popup on the move line, change Quantity
        10 -> 7, save the popup.
Part C: Validate the picking; on the Create Backorder dialog click
        'Create Backorder' (primary).
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    click_status_button,
    ensure_list_view,
    full_url,
    login,
    navigate,
    run_oracle,
    search_for,
    _wait_no_loading,
    _wait_for_ready,
)

ORIGIN = "D-BENCH-PARTIAL-001"


def _open_delivery(page):
    # Navigate to Delivery Orders transfers list.
    page.goto(full_url("/odoo/inventory"), timeout=120000)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Click the Delivery Orders kanban tile.
    delivery_tile = page.locator(
        ".o_kanban_record:has-text('Delivery Orders'), "
        ".o_kanban_primary_right:has-text('Delivery Orders'), "
        ".o_kanban_record .o_primary:has-text('Delivery Orders')"
    ).first
    try:
        delivery_tile.wait_for(state="visible", timeout=10000)
        delivery_tile.click()
    except Exception:
        # Fallback: navigate via the operations menu URL.
        navigate(page, "/odoo/inventory")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(500)
    search_for(page, ORIGIN)
    page.wait_for_timeout(600)
    click_list_row(page, ORIGIN)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)
    _wait_for_ready(page)


def _check_availability(page):
    # Click 'Check Availability' header button.
    btn = page.locator(
        ".o_statusbar_buttons button:has-text('Check Availability'):visible, "
        ".o_form_statusbar button:has-text('Check Availability'):visible, "
        "button[name='action_assign']:visible"
    ).first
    btn.wait_for(state="visible", timeout=15000)
    btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)


def _open_detailed_ops_and_set_qty(page, new_qty):
    # Click Details button on the single move-line row in the Operations tab.
    # In Odoo 19 the button is `action_show_details` with a title "Details".
    details_btn = page.locator(
        ".o_form_view button[name='action_show_details']:visible, "
        ".o_form_view .o_list_renderer button[name='action_show_details']:visible"
    ).first
    details_btn.wait_for(state="visible", timeout=15000)
    details_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    dialog = page.locator(".modal:visible").last

    # The Detailed Operations popup has a move_line_ids list. Find the
    # single existing row and edit its quantity cell.
    rows = dialog.locator(".o_data_row")
    rows.first.wait_for(state="visible", timeout=10000)

    row = rows.first
    qty_cell = row.locator(
        "td[name='quantity']:visible, div[name='quantity']:visible"
    ).first
    qty_cell.click()
    page.wait_for_timeout(300)
    inp = row.locator(
        "td[name='quantity'] input:visible, div[name='quantity'] input:visible"
    ).first
    if inp.count() == 0:
        inp = row.locator("input:visible").first
    inp.press("Control+A")
    inp.press("Meta+A")
    inp.fill(str(new_qty))
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Save / close the popup. The Odoo 19 stock.move "Detailed
    # Operations" dialog is a technical modal with a footer Save +
    # Discard pair; clicking the footer Save closes it.
    # Try the modal-footer Save button first; fall back to keyboard
    # shortcut or the o_form_button_save icon inside the dialog.
    save_btn = dialog.locator(
        ".modal-footer button:has-text('Save & Close'):visible, "
        ".modal-footer button.o_form_button_save:visible, "
        ".modal-footer button:has-text('Save'):visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    try:
        save_btn.click(timeout=5000)
    except Exception:
        # Fallback — press Escape to close (auto-save on close is the
        # default for editable-list x2m dialogs).
        page.keyboard.press("Escape")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # If the modal is still open, force-close with Escape.
    if page.locator(".modal:visible").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    # Also click the outer form save button if the picking form is dirty.
    outer_save = page.locator(
        ".o_form_button_save:visible"
    )
    if outer_save.count() > 0:
        try:
            outer_save.first.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)
        except Exception:
            pass


def _validate_and_backorder(page):
    click_status_button(page, "Validate")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Create Backorder dialog. 'Create Backorder' is the primary button;
    # 'No Backorder' is the secondary.
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
        # Fallback: primary button.
        pbtn = m.locator("button.btn-primary:visible").first
        if pbtn.count() > 0:
            pbtn.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
        else:
            break


def oracle(page):
    login(page)

    _open_delivery(page)
    _check_availability(page)
    _open_detailed_ops_and_set_qty(page, 7)
    _validate_and_backorder(page)


run_oracle(oracle)
