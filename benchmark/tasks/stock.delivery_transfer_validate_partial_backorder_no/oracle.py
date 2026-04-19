"""Oracle for stock.delivery_transfer_validate_partial_backorder_no.

Navigate to the Delivery Orders list, open WH/OUT/BENCH-BACKORDER-NO,
edit the inline Done qty cell 5 -> 3, click Validate, then on the
'Create Backorder?' dialog click the SECONDARY 'No Backorder' button.
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

PICKING_NAME = "WH/OUT/BENCH-BACKORDER-NO"


def _open_delivery(page):
    # Delivery Orders list has path=deliveries
    # (action_picking_tree_outgoing).
    page.goto(full_url("/odoo/inventory/deliveries"), timeout=120000)
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


def _set_done_qty_inline(page, new_qty):
    """Edit the inline Done (`quantity`) cell on the single move row."""
    # Find the move-line row in the Operations tab (picking form's
    # move_ids list). There is a single row.
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row"
    ).first
    row.wait_for(state="visible", timeout=15000)

    qty_cell = row.locator(
        "td[name='quantity']:visible, div[name='quantity']:visible"
    ).first
    qty_cell.click()
    page.wait_for_timeout(400)

    inp = row.locator(
        "td[name='quantity'] input:visible, "
        "div[name='quantity'] input:visible"
    ).first
    if inp.count() == 0:
        inp = row.locator("input:visible").first
    # Clear + fill.
    inp.press("Control+A")
    inp.press("Meta+A")
    inp.fill(str(new_qty))
    inp.press("Tab")
    page.wait_for_timeout(700)
    _wait_no_loading(page)


def _validate_and_no_backorder(page):
    click_status_button(page, "Validate")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Create Backorder dialog. 'Create Backorder' is primary (DEFAULT);
    # 'No Backorder' is secondary. We must click 'No Backorder'.
    for _ in range(3):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        m = modal.last
        no_bo = m.locator("button:has-text('No Backorder'):visible")
        if no_bo.count() > 0:
            no_bo.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
            continue
        # Fallback — if for some reason only a single primary button
        # shows up (e.g., validation error modal), click it.
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
    _set_done_qty_inline(page, 3)
    _validate_and_no_backorder(page)


run_oracle(oracle)
