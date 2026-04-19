"""Oracle for stock.receipt_full_quantity_validate_no_backorder.

Navigate to the Receipts list, open WH/IN/BENCH-FULL, click Validate in
the header. No dialog should appear (Done 10 == Demand 10). The picking
flips to Done.
"""

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

PICKING_NAME = "WH/IN/BENCH-FULL"


def _open_receipt(page):
    # Receipts list has path=receipts (action_picking_tree_incoming).
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


def _validate(page):
    click_status_button(page, "Validate")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Defensive: no backorder dialog is expected, but if a wizard ever
    # surfaces (e.g., availability prompt on some base snapshots), click
    # through with the primary action.
    for _ in range(2):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        m = modal.last
        # Prefer "Apply" / "Validate" / primary.
        btn = m.locator(
            "button:has-text('Apply'):visible, "
            "button:has-text('Validate'):visible, "
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
    _validate(page)


run_oracle(oracle)
