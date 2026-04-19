"""Oracle for purchase.confirm_rfq_receive_full_three_way_match.

Steps:
  1. Navigate to /odoo/purchase, open RFQ with Vendor Reference
     'BENCH-RFQ-3WAY-2'.
  2. Click Confirm Order in the form's status bar.
  3. Click the Receive Products smart button (name='action_view_picking').
  4. On the auto-generated receipt, click Validate (no edits — the full
     demand pre-fills the Done qty columns).
"""

from benchmark.oracle_helpers import (
    click_button_name,
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


RFQ_REF = "BENCH-RFQ-3WAY-2"


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)
    page.wait_for_timeout(600)

    click_list_row(page, RFQ_REF)
    page.wait_for_timeout(1200)
    _wait_for_ready(page)

    # Part A: Confirm Order
    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1800)
    _wait_no_loading(page)

    # Handle any confirmation modal (alternatives wizard etc.; harmless
    # fall-through if none appears).
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        pbtn = modal.last.locator("button.btn-primary:visible").first
        if pbtn.count() > 0:
            try:
                pbtn.click()
                page.wait_for_timeout(800)
                _wait_no_loading(page)
            except Exception:
                pass

    # Part B: open the auto-generated receipt via the smart button.
    # On a single-picking PO, action_view_picking redirects straight to
    # the stock.picking form.
    try:
        click_button_name(page, "action_view_picking")
    except Exception:
        # Fallback selector combinations for the smart button.
        smart_btn = page.locator(
            ".oe_stat_button:visible:has-text('Receive Products'), "
            ".oe_stat_button:visible:has-text('Receive'), "
            ".o_statusbar_buttons button:visible:has-text('Receive'), "
            "button[name='action_view_picking']:visible"
        ).first
        smart_btn.wait_for(state="visible", timeout=15000)
        smart_btn.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)
    _wait_no_loading(page)

    # If the smart button landed us on a list (e.g. multiple receipts
    # — shouldn't happen here) pick the first row.
    list_rows = page.locator(".o_list_view .o_data_row")
    if list_rows.count() > 0 and page.locator(".o_form_view").count() == 0:
        list_rows.first.click()
        page.wait_for_timeout(1000)
        _wait_for_ready(page)

    # Part C: Validate the receipt. Full demand pre-fills; no cell-edit.
    click_status_button(page, "Validate")
    page.wait_for_timeout(1800)
    _wait_no_loading(page)

    # Handle any secondary modal (e.g. "Immediate Transfer?" confirmation
    # — accept the primary button; no backorder expected on full-demand
    # receipts).
    for _ in range(2):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        m = modal.last
        pbtn = m.locator("button.btn-primary:visible").first
        if pbtn.count() == 0:
            break
        try:
            pbtn.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)
        except Exception:
            break


run_oracle(oracle)
