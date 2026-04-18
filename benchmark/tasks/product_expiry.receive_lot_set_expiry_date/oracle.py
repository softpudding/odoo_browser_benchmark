"""Oracle for product_expiry.receive_lot_set_expiry_date.

Open receipt BENCH-PERISH-RCV-01, click the Details button on the
Bench Perishable move line, create lot BP-LOT-001 on the fly in the
popup's lot_id m2o, click the internal-link arrow to open the
stock.lot nested dialog, set expiration_date (today+60) and
removal_date (today+55), save the lot dialog, save the popup, then
Validate the receipt.
"""

from datetime import datetime, timedelta

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    click_status_button,
    ensure_list_view,
    full_url,
    login,
    run_oracle,
    search_for,
    _wait_no_loading,
    _wait_for_ready,
)


LOT_NAME = "BP-LOT-001"
ORIGIN = "BENCH-PERISH-RCV-01"


def _fmt(dt):
    return dt.strftime("%m/%d/%Y %H:%M:%S")


def _open_receipt(page):
    page.goto(full_url("/odoo/inventory/receipts"), timeout=120000)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(300)

    search_for(page, ORIGIN)
    page.wait_for_timeout(600)

    click_list_row(page, ORIGIN)
    page.wait_for_timeout(900)
    _wait_no_loading(page)


def _open_details_popup(page):
    details = page.locator("button[name='action_show_details']:visible")
    details.first.wait_for(state="visible", timeout=15000)
    details.first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def _create_lot_in_popup(page):
    dialog = page.locator(".modal:visible").last
    rows = dialog.locator(".o_data_row")
    if rows.count() == 0:
        # Odoo may auto-create one move_line_row during assign; if not,
        # add one.
        add_btn = dialog.locator(
            "a:has-text('Add a line'):visible, "
            "button:has-text('Add a line'):visible"
        )
        if add_btn.count() > 0:
            add_btn.first.click()
            page.wait_for_timeout(500)
            rows = dialog.locator(".o_data_row")

    row = rows.first

    # Click the lot cell.
    lot_cell = row.locator(
        "div[name='lot_id']:visible, td[name='lot_id']:visible"
    ).first
    if lot_cell.count() == 0:
        # Fallback to lot_name cell if lot_id isn't rendered.
        lot_cell = row.locator(
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
    inp.fill(LOT_NAME)
    page.wait_for_timeout(800)

    # Pick the 'Create "BP-LOT-001"' autocomplete option.
    create_opt = page.locator(
        '.o-autocomplete--dropdown-item:has-text("Create"):visible'
    )
    if create_opt.count() > 0:
        create_opt.first.click()
    else:
        inp.press("Enter")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def _open_lot_nested_dialog(page):
    dialog = page.locator(".modal:visible").last
    row = dialog.locator(".o_data_row").first

    # Click into the lot cell to ensure the widget is active and the
    # internal-link button is rendered.
    lot_cell = row.locator(
        "div[name='lot_id']:visible, td[name='lot_id']:visible"
    ).first
    lot_cell.click()
    page.wait_for_timeout(400)

    # The external (internal-link) button on the many2one.
    ext_btn = lot_cell.locator(
        "button.o_external_button:visible, "
        ".o_external_button:visible, "
        "button:has(.oi-launch):visible, "
        "button:has(.oi-arrow-right):visible"
    ).first
    ext_btn.wait_for(state="visible", timeout=10000)
    ext_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def _set_datetime_in_dialog(page, dialog, field_name, value_str):
    # Odoo 19 DateTimeField: when the field has a value and is not the
    # active input, it renders as <button> showing the formatted value.
    # Click the button to switch it into <input>, THEN type.
    widget = dialog.locator(
        f".o_field_widget[name='{field_name}']"
    ).first
    widget.scroll_into_view_if_needed(timeout=5000)

    # Click either the button OR the input (whichever is rendered).
    btn_or_inp = widget.locator("button, input").first
    btn_or_inp.wait_for(state="visible", timeout=10000)
    btn_or_inp.click()
    page.wait_for_timeout(400)

    # After click, an input should now exist.
    inp = widget.locator("input").first
    inp.wait_for(state="visible", timeout=5000)
    inp.click()
    page.wait_for_timeout(100)
    # Select all + clear (macOS vs linux).
    inp.press("Meta+A")
    inp.press("Control+A")
    inp.fill("")
    # Type the new value slowly to allow Odoo to parse.
    inp.type(value_str, delay=20)
    # Close the picker popover — Escape keeps the value.
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    # Click elsewhere to commit.
    try:
        dialog.locator(".modal-title").first.click()
    except Exception:
        pass
    page.wait_for_timeout(300)


def _set_lot_expiration(page):
    # Wait for the nested stock.lot dialog to actually be loaded.
    # There may be several nested .modal elements — identify the one
    # containing the stock.lot form fields (product_id + expiration).
    page.wait_for_timeout(800)
    # Pick the last visible modal that contains the expiration_date field.
    lot_dialog = None
    modals = page.locator(".modal:visible")
    count = modals.count()
    for i in range(count - 1, -1, -1):
        m = modals.nth(i)
        # Look for any stock.lot-specific marker — e.g. name is `Lot` in the title,
        # or expiration_date widget exists even if not yet "visible".
        title = (m.locator(".modal-title").inner_text() or "").strip() if m.locator(".modal-title").count() > 0 else ""
        has_exp = m.locator(".o_field_widget[name='expiration_date']").count() > 0
        if has_exp or ("Lot" in title and "BP-LOT-001" in (m.inner_text() or "")):
            lot_dialog = m
            break
    if lot_dialog is None:
        # Fallback: use the last modal (which should be on top).
        lot_dialog = modals.last

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    expiration = today + timedelta(days=60)
    removal = today + timedelta(days=55)

    _set_datetime_in_dialog(
        page, lot_dialog, "expiration_date", _fmt(expiration)
    )
    _set_datetime_in_dialog(
        page, lot_dialog, "removal_date", _fmt(removal)
    )

    # Save the lot dialog. The footer button may read 'Save & Close'
    # or 'Save'; fall back to the primary footer button.
    save_btn = lot_dialog.locator(
        ".modal-footer button.btn-primary:has-text('Save & Close'):visible, "
        ".modal-footer button.btn-primary:has-text('Save'):visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    save_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def _save_details_popup(page):
    # After the lot dialog closes, the details popup becomes the top
    # modal again.
    dialog = page.locator(".modal:visible").last
    save_btn = dialog.locator(
        ".modal-footer button.btn-primary:has-text('Save'):visible, "
        "button.o_form_button_save:visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    save_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def _validate_picking(page):
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # Save the picking form first so move_line edits are persisted.
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

    # Handle any confirmation / backorder modal. There's no backorder
    # because demand==done, but an Apply dialog may appear.
    for _ in range(3):
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
    _open_details_popup(page)
    _create_lot_in_popup(page)
    _open_lot_nested_dialog(page)
    _set_lot_expiration(page)
    _save_details_popup(page)
    _validate_picking(page)


run_oracle(oracle)
