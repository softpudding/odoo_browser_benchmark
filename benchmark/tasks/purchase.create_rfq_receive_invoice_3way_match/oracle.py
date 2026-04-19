"""Oracle for purchase.create_rfq_receive_invoice_3way_match.

Part A: create RFQ (vendor Bench Supply Co + 2 lines) -> Confirm Order.
Part B: open Receipt smart button, set Done=7 on Item A (leave B=5),
        Validate, pick Create Backorder.
Part C: navigate to Purchase Orders list, select the PO checkbox,
        click Create Bills, set Bill Date + Bill Reference, Confirm.
"""

from datetime import date

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_date,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


VENDOR_NAME = "Bench Supply Co"
LINES = [
    ("Bench PO Item A", "10", "20.00"),
    ("Bench PO Item B", "5", "40.00"),
]
BILL_REF = "BSC-BILL-3WM"


def _set_done_qty_row(page, row_index, value):
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row, "
        ".o_list_view .o_data_row"
    ).nth(row_index)
    cell = row.locator(
        "td[name='quantity'], .o_field_widget[name='quantity']"
    ).first
    cell.click()
    page.wait_for_timeout(250)
    inp = cell.locator("input").first
    if inp.count() == 0:
        inp = row.locator("input:visible").first
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def _part_a_create_and_confirm_rfq(page):
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_create(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    set_many2one(page, "partner_id", VENDOR_NAME)
    page.wait_for_timeout(700)

    for i, (product, qty, price) in enumerate(LINES):
        click_add_a_line(page)
        page.wait_for_timeout(500)
        set_o2m_many2one(page, i, "product_id", product)
        page.wait_for_timeout(500)
        set_o2m_field(page, i, "product_qty", qty)
        page.wait_for_timeout(300)
        set_o2m_field(page, i, "price_unit", price)
        page.wait_for_timeout(300)

    # Persist the form before clicking Confirm.
    save_btn = page.locator(".o_form_button_save:visible")
    if save_btn.count() > 0:
        try:
            save_btn.first.click()
            page.wait_for_timeout(600)
            _wait_no_loading(page)
        except Exception:
            pass

    confirm_btn = page.locator(
        "button[name='button_confirm']:visible, "
        "button:has-text('Confirm Order'):visible"
    ).first
    confirm_btn.click()
    page.wait_for_timeout(1800)
    _wait_no_loading(page)

    # Any residual confirmation modal (alternatives wizard etc.)
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        pbtn = modal.last.locator("button.btn-primary:visible").first
        if pbtn.count() > 0:
            try:
                pbtn.click()
                page.wait_for_timeout(1000)
                _wait_no_loading(page)
            except Exception:
                pass


def _part_b_receive_with_backorder(page):
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

    # Set Done=7 on row 0 (Item A). Leave row 1 (Item B) at default 5.
    _set_done_qty_row(page, 0, "7")

    save_btn = page.locator(".o_form_button_save:visible")
    if save_btn.count() > 0:
        try:
            save_btn.first.click()
            page.wait_for_timeout(600)
            _wait_no_loading(page)
        except Exception:
            pass

    click_status_button(page, "Validate")
    page.wait_for_timeout(1800)
    _wait_no_loading(page)

    # Create Backorder dialog
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
        pbtn = m.locator("button.btn-primary:visible").first
        if pbtn.count() > 0:
            pbtn.click()
            page.wait_for_timeout(1200)
            _wait_no_loading(page)
        else:
            break


def _part_c_create_and_post_bill(page):
    # In Odoo 19 the PO form itself has no 'Create Bill' button; the
    # action lives in the Purchase Orders list view: select the PO
    # checkbox + click 'Create Bills' in the list header. With one PO
    # selected, Odoo redirects to the generated bill's form view.
    navigate(page, "/odoo/purchase-orders")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    row = page.locator(
        f".o_list_view .o_data_row:has-text('{VENDOR_NAME}')"
    ).first
    row.wait_for(state="visible", timeout=15000)
    row.locator(".o_list_record_selector input[type='checkbox']").first.click()
    page.wait_for_timeout(600)

    create_btn = page.locator(
        "button[name='action_create_invoice']:visible, "
        ".o_list_view button:has-text('Create Bills'):visible, "
        ".o_control_panel button:has-text('Create Bills'):visible"
    ).first
    create_btn.wait_for(state="visible", timeout=15000)
    create_btn.click()
    page.wait_for_timeout(3000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    page.locator(".o_form_view").first.wait_for(
        state="visible", timeout=15000
    )

    # Set Bill Date first — opening the date widget triggers the Owl form
    # into "edit" mode so the subsequent `ref` edit is tracked as dirty.
    # (fill_field alone on a freshly-opened v19 bill form often leaves
    # the form considered clean and the Save button stays disabled.)
    today = date.today()
    date_str = f"{today.month:02d}/{today.day:02d}/{today.year}"
    try:
        set_date(page, "invoice_date", date_str)
    except Exception:
        pass

    fill_field(page, "ref", BILL_REF)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Save the form if the Save button is visible; otherwise rely on
    # action_post's auto-save.
    save_btn = page.locator(".o_form_button_save:visible")
    if save_btn.count() > 0:
        try:
            save_btn.first.click(timeout=3000)
            page.wait_for_timeout(1200)
            _wait_no_loading(page)
        except Exception:
            pass

    # Click Confirm (aka action_post for move_type != 'entry').
    confirm_btn = page.locator(
        "button[name='action_post']:visible"
    ).first
    confirm_btn.wait_for(state="visible", timeout=15000)
    confirm_btn.click()
    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    # Handle any secondary confirmation modal (e.g., duplicate warning).
    for _ in range(2):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        pbtn = modal.last.locator("button.btn-primary:visible").first
        if pbtn.count() == 0:
            break
        try:
            pbtn.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)
        except Exception:
            break


def oracle(page):
    login(page)
    _part_a_create_and_confirm_rfq(page)
    _part_b_receive_with_backorder(page)
    _part_c_create_and_post_bill(page)


run_oracle(oracle)
