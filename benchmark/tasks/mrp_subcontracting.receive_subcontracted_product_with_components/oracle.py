"""Oracle for mrp_subcontracting.receive_subcontracted_product_with_components.

Open the receipt generated from PO P-BENCH-SUB-001 (serial-tracked
'Bench Sub Assembly' qty=2), open Detailed Operations on the move line,
enter BSA-2026-01 / BSA-2026-02 (qty 1 each) via Create autocomplete,
save, then Validate. This triggers auto-close of the subcontract MO
and back-flushes 2x Part-A and 2x Part-B from the subcontracting
location.
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

PO_NAME = "P-BENCH-SUB-001"
SERIALS = ("BSA-2026-01", "BSA-2026-02")


def _open_receipts_list(page):
    page.goto(full_url("/odoo/inventory/receipts"), timeout=120000)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def _open_receipt(page):
    _open_receipts_list(page)
    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(300)

    search_for(page, PO_NAME)
    page.wait_for_timeout(700)

    click_list_row(page, PO_NAME)
    page.wait_for_timeout(1200)
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


def _enter_two_serials(page):
    """Open Detailed Operations, enter two serials, save popup."""
    # Click the row's Details button (action_show_details).
    details = page.locator("button[name='action_show_details']:visible")
    details.first.wait_for(state="visible", timeout=15000)
    details.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    dialog = page.locator(".modal:visible").last

    ml_rows = dialog.locator(".o_data_row")
    while ml_rows.count() < 2:
        add_btn = dialog.locator(
            "a:has-text('Add a line'):visible, "
            "button:has-text('Add a line'):visible"
        ).first
        add_btn.click()
        page.wait_for_timeout(600)
        ml_rows = dialog.locator(".o_data_row")

    while ml_rows.count() > 2:
        last = ml_rows.last
        trash = last.locator(
            ".o_list_record_remove, .fa-trash-o, "
            "button.o_list_record_remove"
        )
        if trash.count() == 0:
            break
        trash.first.click()
        page.wait_for_timeout(400)
        ml_rows = dialog.locator(".o_data_row")

    for i, sn in enumerate(SERIALS):
        ml_rows = dialog.locator(".o_data_row")
        row = ml_rows.nth(i)
        _fill_row_lot_name(page, row, sn)
        _fill_row_qty(page, row, "1")

    # Remove any extra rows without serials.
    page.wait_for_timeout(500)
    ml_rows = dialog.locator(".o_data_row")
    for i in range(ml_rows.count() - 1, -1, -1):
        row = ml_rows.nth(i)
        text = (row.inner_text() or "").strip()
        if not any(sn in text for sn in SERIALS):
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


def _validate(page):
    # Save form first.
    save_btn = page.locator(".o_form_button_save:visible")
    if save_btn.count() > 0:
        try:
            save_btn.first.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)
        except Exception:
            pass

    click_status_button(page, "Validate")
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # Handle any follow-up dialog.
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
    _open_receipt(page)
    _enter_two_serials(page)
    _validate(page)


run_oracle(oracle)
