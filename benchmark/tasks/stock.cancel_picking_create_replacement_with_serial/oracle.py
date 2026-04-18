"""Oracle for stock.cancel_picking_create_replacement_with_serial.

Part A: open receipt R-BENCH-CANCEL-001 and Cancel it.
Part B: create a new receipt for Bench Supplier Inc, one line for
        Bench Serial Widget demand=2, Confirm it.
Part C: open Detailed Operations on that move line, ensure 2 move-line
        rows exist (add one), enter BS-001 / BS-002 + qty 1 each, save.
Part D: Validate.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    clear_search_filters,
    ensure_list_view,
    full_url,
    login,
    run_oracle,
    save_form,
    search_for,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)

ORIGIN = "R-BENCH-CANCEL-001"
VENDOR = "Bench Supplier Inc"
SERIAL_PRODUCT = "Bench Serial Widget"
SERIALS = ("BS-001", "BS-002")


def _open_receipts_list(page):
    # Receipts list has path=receipts (action_picking_tree_incoming).
    page.goto(full_url("/odoo/inventory/receipts"), timeout=120000)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def _cancel_original(page):
    _open_receipts_list(page)
    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(300)

    search_for(page, ORIGIN)
    page.wait_for_timeout(600)

    click_list_row(page, ORIGIN)
    page.wait_for_timeout(900)
    _wait_no_loading(page)

    # Click Cancel button in header.
    click_status_button(page, "Cancel")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # A confirmation dialog may appear.
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        ok_btn = modal.last.locator(
            "button:has-text('Ok'):visible, "
            "button:has-text('Confirm'):visible, "
            "button:has-text('Yes'):visible, "
            "button.btn-primary:visible"
        ).first
        if ok_btn.count() > 0:
            ok_btn.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)


def _fill_row_qty(page, row, value):
    qty_cell = row.locator(
        "div[name='quantity']:visible, td[name='quantity']:visible"
    ).first
    qty_cell.click()
    page.wait_for_timeout(300)
    inp = row.locator(
        "div[name='quantity'] input:visible, td[name='quantity'] input:visible"
    ).first
    if inp.count() == 0:
        inp = row.locator("input:visible").first
    inp.press("Control+A")
    inp.press("Meta+A")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def _fill_row_lot_name(page, row, value):
    lot_cell = row.locator(
        "div[name='lot_name']:visible, td[name='lot_name']:visible, "
        "div[name='lot_id']:visible, td[name='lot_id']:visible"
    ).first
    lot_cell.click()
    page.wait_for_timeout(300)
    inp = row.locator(
        "div[name='lot_name'] input:visible, "
        "div[name='lot_id'] input:visible"
    ).first
    if inp.count() == 0:
        inp = row.locator("input:visible").first
    inp.fill(value)
    page.wait_for_timeout(700)

    create_opt = page.locator(
        '.o-autocomplete--dropdown-item:has-text("Create"):visible'
    )
    if create_opt.count() > 0:
        create_opt.first.click()
    else:
        inp.press("Enter")
    page.wait_for_timeout(700)
    _wait_no_loading(page)


def _create_new_receipt(page):
    # Back to the receipts list via breadcrumb or navigation.
    # After cancelling the original, we are still on its form. Use the
    # action URL for receipts (Receipt picking type action tag).
    picking_type_id = None
    # Try to find Receipts picking type id via the pickings kanban.
    # Simpler: navigate to inventory dashboard and click the Receipts kanban.
    _open_receipts_list(page)
    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    # Click the top-left New button on the list view.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_list_button_add:visible, "
        ".o_cp_buttons button:has-text('New'):visible, "
        ".o_control_panel button:has-text('New'):visible, "
        ".o-kanban-button-new:visible"
    ).first
    new_btn.wait_for(state="visible", timeout=20000)
    new_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # On the form, set Receive From (partner_id) to the vendor.
    set_many2one(page, "partner_id", VENDOR)
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # Add a product line on the Operations tab. The label is "Add a Product"
    # (stock.picking move_ids list has add-label="Add a Product").
    add_line = page.locator(
        ".o_form_view .o_list_renderer a:has-text('Add a Product'):visible, "
        ".o_form_view .o_list_renderer button:has-text('Add a Product'):visible, "
        ".o_field_x2many a:has-text('Add a Product'):visible, "
        ".o_field_x2many a:has-text('Add a line'):visible"
    ).first
    add_line.click()
    page.wait_for_timeout(800)

    # Set product in the newly added row via the o2m helper.
    set_o2m_many2one(page, 0, "product_id", SERIAL_PRODUCT)
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    # Set demand (product_uom_qty) to 2.
    set_o2m_field(page, 0, "product_uom_qty", "2")
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # Save the form to persist the picking as draft.
    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Confirm the picking via the header button.
    # In Odoo 19 the receipt form header uses "Mark as Todo" for action_confirm.
    for label in ("Mark as Todo", "Confirm"):
        btn = page.locator(
            f".o_statusbar_buttons button:has-text('{label}'):visible, "
            f".o_form_statusbar button:has-text('{label}'):visible"
        )
        if btn.count() > 0:
            btn.first.click()
            page.wait_for_timeout(1800)
            _wait_no_loading(page)
            break


def _enter_two_serials(page):
    # Open Detailed Operations via the Details button on the move line.
    details = page.locator(
        "button[name='action_show_details']:visible"
    )
    details.first.wait_for(state="visible", timeout=15000)
    details.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    dialog = page.locator(".modal:visible").last

    # The move form dialog contains an inner move_line_ids list.
    # With tracking='serial' and demand=2, action_assign auto-reserves
    # two move_lines (empty lot, qty 1 each) — we just fill lot_name.
    ml_rows = dialog.locator(".o_data_row")
    rows_count = ml_rows.count()

    # Ensure we end up with EXACTLY 2 rows in the popup.
    while rows_count < 2:
        add_btn = dialog.locator(
            "a:has-text('Add a line'):visible, "
            "button:has-text('Add a line'):visible"
        ).first
        add_btn.click()
        page.wait_for_timeout(600)
        ml_rows = dialog.locator(".o_data_row")
        rows_count = ml_rows.count()

    # Remove any extra rows beyond 2 (shouldn't happen, defensive).
    while ml_rows.count() > 2:
        last = ml_rows.last
        trash = last.locator(".o_list_record_remove, .fa-trash-o, button.o_list_record_remove")
        if trash.count() == 0:
            break
        trash.first.click()
        page.wait_for_timeout(400)
        ml_rows = dialog.locator(".o_data_row")

    # Fill BS-001 / BS-002 on each row, qty 1 each.
    for i, sn in enumerate(SERIALS):
        ml_rows = dialog.locator(".o_data_row")
        row = ml_rows.nth(i)
        _fill_row_lot_name(page, row, sn)
        _fill_row_qty(page, row, "1")

    # After filling row 2, editable-bottom lists sometimes append a new empty
    # row. Remove any rows with empty lot_name / qty == 0.
    page.wait_for_timeout(500)
    ml_rows = dialog.locator(".o_data_row")
    for i in range(ml_rows.count() - 1, -1, -1):
        row = ml_rows.nth(i)
        text = (row.inner_text() or "").strip()
        has_serial = any(s in text for s in SERIALS)
        if not has_serial:
            # empty row — remove it via trash/delete.
            trash = row.locator(
                ".o_list_record_remove, .fa-trash-o, "
                "button.o_list_record_remove, button[name='delete']"
            )
            if trash.count() > 0:
                try:
                    trash.first.click()
                    page.wait_for_timeout(400)
                except Exception:
                    pass

    # Save / close the dialog.
    save_btn = dialog.locator(
        ".modal-footer button.btn-primary:has-text('Save'):visible, "
        "button.o_form_button_save:visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    save_btn.click()
    page.wait_for_timeout(1800)
    _wait_no_loading(page)


def _validate_and_finish(page):
    # Ensure any prior popup is closed before clicking Validate.
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Save the form first so move_line edits are persisted.
    save_form_btn = page.locator(
        ".o_form_button_save:visible"
    )
    if save_form_btn.count() > 0:
        try:
            save_form_btn.first.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)
        except Exception:
            pass

    click_status_button(page, "Validate")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Handle confirmation / backorder / immediate-transfer / serial-error modal.
    for _ in range(4):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        m = modal.last

        no_bo = m.locator("button:has-text('No Backorder'):visible")
        if no_bo.count() > 0:
            no_bo.first.click()
            page.wait_for_timeout(1200)
            _wait_no_loading(page)
            continue

        btn = m.locator(
            "button:has-text('Apply'):visible, "
            "button:has-text('Validate'):visible, "
            "button:has-text('Confirm'):visible, "
            "button:has-text('Ok'):visible, "
            "button.btn-primary:visible"
        ).first
        if btn.count() > 0:
            btn.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
        else:
            break


def oracle(page):
    login(page)

    _cancel_original(page)
    _create_new_receipt(page)
    _enter_two_serials(page)
    _validate_and_finish(page)


run_oracle(oracle)
