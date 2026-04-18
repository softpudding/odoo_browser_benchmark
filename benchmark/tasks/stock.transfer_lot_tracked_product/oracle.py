"""Oracle for stock.transfer_lot_tracked_product.

Open receipt BENCH-TRANSFER-LOT-01, on the Lot Product A move line set
quantity=50 and lot=LOT-2026-001 (creating the lot on the fly), then
Validate without creating a backorder.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)

LOT_NAME = "LOT-2026-001"
ORIGIN = "BENCH-TRANSFER-LOT-01"
QTY = "50"


def _fill_row_quantity(page, row, value):
    """Try to fill the quantity cell directly on the move line row."""
    qty_cell = row.locator(
        "div[name='quantity']:visible, td[name='quantity']:visible"
    ).first
    if qty_cell.count() == 0:
        return False
    qty_cell.click()
    page.wait_for_timeout(300)
    qty_input = row.locator("div[name='quantity'] input:visible").first
    if qty_input.count() == 0:
        qty_input = row.locator("td[name='quantity'] input:visible").first
    if qty_input.count() == 0:
        return False
    qty_input.press("Control+A")
    qty_input.press("Meta+A")
    qty_input.fill(value)
    qty_input.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)
    return True


def _fill_row_lot(page, row, lot_name):
    """Type lot_name into the lot cell and accept the Create option."""
    lot_cell = row.locator(
        "div[name='lot_id']:visible, "
        "td[name='lot_id']:visible, "
        "div[name='lot_name']:visible, "
        "td[name='lot_name']:visible"
    ).first
    if lot_cell.count() == 0:
        return False
    lot_cell.click()
    page.wait_for_timeout(400)

    inp = row.locator(
        "div[name='lot_id'] input:visible, "
        "div[name='lot_name'] input:visible"
    ).first
    if inp.count() == 0:
        inp = row.locator("input:visible").first
    inp.fill(lot_name)
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
    return True


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Click the Receipts kanban tile
    cards = page.locator(".o_kanban_record:visible")
    for i in range(cards.count()):
        if "Receipts" in cards.nth(i).inner_text():
            cards.nth(i).click()
            break
    _wait_no_loading(page)
    page.wait_for_timeout(700)

    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(300)

    click_list_row(page, ORIGIN)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Try the inline row approach first; if quantity cell isn't present
    # (some views hide it), fall back to the Details button popup.
    rows = page.locator(
        ".o_form_view .o_list_renderer .o_data_row"
    )
    row_used = None
    if rows.count() > 0:
        row_used = rows.first

    used_dialog = False
    if row_used is not None:
        ok_qty = _fill_row_quantity(page, row_used, QTY)
        ok_lot = _fill_row_lot(page, row_used, LOT_NAME)
        if not (ok_qty and ok_lot):
            used_dialog = True
    else:
        used_dialog = True

    if used_dialog:
        # Open the Details popup on the move line
        details = page.locator(
            "button[name='action_show_details']:visible"
        )
        details.first.click()
        page.wait_for_timeout(1200)
        _wait_no_loading(page)
        dialog = page.locator(".modal:visible").last

        ml_rows = dialog.locator(".o_data_row")
        if ml_rows.count() == 0:
            add_btn = dialog.locator(
                "a:has-text('Add a line'):visible, "
                "button:has-text('Add a line'):visible"
            )
            if add_btn.count() > 0:
                add_btn.first.click()
                page.wait_for_timeout(500)
                ml_rows = dialog.locator(".o_data_row")

        row = ml_rows.last
        _fill_row_lot(page, row, LOT_NAME)
        _fill_row_quantity(page, row, QTY)

        save_btn = dialog.locator(
            "button.btn-primary:has-text('Save'):visible, "
            "button.o_form_button_save:visible, "
            "button.btn-primary:visible"
        ).first
        save_btn.click()
        page.wait_for_timeout(1200)
        _wait_no_loading(page)

    # Validate
    click_status_button(page, "Validate")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Handle any dialog that appears: prefer "No Backorder"
    for _ in range(3):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        m = modal.last
        no_bo = m.locator(
            "button:has-text('No Backorder'):visible, "
            "button:has-text(\"No backorder\"):visible"
        )
        if no_bo.count() > 0:
            no_bo.first.click()
            page.wait_for_timeout(1200)
            _wait_no_loading(page)
            continue
        # Fallback: any primary action
        btn = m.locator(
            "button:has-text('Apply'):visible, "
            "button:has-text('Validate'):visible, "
            "button:has-text('Confirm'):visible, "
            "button.btn-primary:visible"
        ).first
        if btn.count() > 0:
            btn.click()
            page.wait_for_timeout(1200)
            _wait_no_loading(page)
        else:
            break


run_oracle(oracle)
