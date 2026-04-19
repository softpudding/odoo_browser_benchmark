"""Oracle for stock.receive_serial_tracked_product_two_serials.

Open the pre-seeded WH/IN/BENCH-SERIAL receipt. Click the Details
button on the Bench Serial Item move line. In the modal, ensure 2
move_line rows; fill SN-BENCH-A001 / SN-BENCH-A002 (qty 1 each),
picking the `Create "<serial>"` autocomplete option. Sweep any
empty trailing rows. Save + close. Back on the picking, click
Validate. Handle any terminal "No Backorder" / confirmation modal
defensively.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    clear_search_filters,
    ensure_list_view,
    full_url,
    login,
    run_oracle,
    search_for,
    _wait_no_loading,
    _wait_for_ready,
)

PICKING_NAME = "WH/IN/BENCH-SERIAL"
SERIALS = ("SN-BENCH-A001", "SN-BENCH-A002")


def _open_picking(page):
    page.goto(full_url("/odoo/inventory/receipts"), timeout=120000)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(500)
    search_for(page, PICKING_NAME)
    page.wait_for_timeout(800)
    click_list_row(page, PICKING_NAME)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)
    _wait_for_ready(page)


def _fill_row_qty(page, row, value):
    qty_cell = row.locator(
        "div[name='quantity']:visible, td[name='quantity']:visible"
    ).first
    qty_cell.click()
    page.wait_for_timeout(300)
    inp = row.locator(
        "div[name='quantity'] input:visible, "
        "td[name='quantity'] input:visible"
    ).first
    if inp.count() == 0:
        inp = row.locator("input:visible").first
    inp.press("Control+A")
    inp.press("Meta+A")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def _fill_row_lot(page, row, value):
    lot_cell = row.locator(
        "div[name='lot_id']:visible, td[name='lot_id']:visible, "
        "div[name='lot_name']:visible, td[name='lot_name']:visible"
    ).first
    lot_cell.click()
    page.wait_for_timeout(300)
    inp = row.locator(
        "div[name='lot_id'] input:visible, "
        "div[name='lot_name'] input:visible"
    ).first
    if inp.count() == 0:
        inp = row.locator("input:visible").first
    inp.fill(value)
    page.wait_for_timeout(800)

    create_opt = page.locator(
        '.o-autocomplete--dropdown-item:has-text("Create"):visible'
    )
    if create_opt.count() > 0:
        create_opt.first.click()
    else:
        inp.press("Enter")
    page.wait_for_timeout(700)
    _wait_no_loading(page)


def _enter_serials(page):
    # Open Detailed Operations via the Details button on the move line.
    details = page.locator("button[name='action_show_details']:visible")
    details.first.wait_for(state="visible", timeout=15000)
    details.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    dialog = page.locator(".modal:visible").last

    # Ensure we have exactly 2 move_line rows in the popup.
    ml_rows = dialog.locator(".o_data_row")
    rows_count = ml_rows.count()
    while rows_count < 2:
        add_btn = dialog.locator(
            "a:has-text('Add a line'):visible, "
            "button:has-text('Add a line'):visible"
        ).first
        add_btn.click()
        page.wait_for_timeout(600)
        ml_rows = dialog.locator(".o_data_row")
        rows_count = ml_rows.count()

    # Fill SN-BENCH-A001 / SN-BENCH-A002 with qty=1 each.
    for i, sn in enumerate(SERIALS):
        ml_rows = dialog.locator(".o_data_row")
        row = ml_rows.nth(i)
        _fill_row_lot(page, row, sn)
        _fill_row_qty(page, row, "1")

    # After filling, editable-bottom lists sometimes append a new empty
    # row. Remove any rows that don't carry one of our serials.
    page.wait_for_timeout(500)
    ml_rows = dialog.locator(".o_data_row")
    for i in range(ml_rows.count() - 1, -1, -1):
        row = ml_rows.nth(i)
        text = (row.inner_text() or "").strip()
        has_serial = any(s in text for s in SERIALS)
        if not has_serial:
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

    # Save the popup.
    save_btn = dialog.locator(
        ".modal-footer button.btn-primary:has-text('Save'):visible, "
        "button.o_form_button_save:visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    save_btn.click()
    page.wait_for_timeout(1800)
    _wait_no_loading(page)

    # Dialog should now be closed; if still present (editable-x2m
    # sometimes lingers), Escape it.
    leftover = page.locator(".modal:visible")
    if leftover.count() > 0:
        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(600)
            _wait_no_loading(page)
        except Exception:
            pass


def _validate(page):
    # Save the outer form first so move_line edits persist before
    # button_validate fires.
    save_form_btn = page.locator(".o_form_button_save:visible")
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

    _open_picking(page)
    _enter_serials(page)
    _validate(page)


run_oracle(oracle)
