"""Oracle for stock.cancel_picking_abandoned.

Navigate to the Delivery Orders list, open WH/OUT/BENCH-CANCEL, click
the statusbar Cancel button, and confirm the 'Are you sure you want to
cancel this transfer?' dialog so state becomes 'cancel'.
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

PICKING_NAME = "WH/OUT/BENCH-CANCEL"


def _open_delivery(page):
    # Delivery Orders list (action_picking_tree_outgoing → path="deliveries").
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


def _cancel_and_confirm(page):
    # The statusbar Cancel button opens an "Are you sure you want to cancel
    # this transfer?" dialog (declared via confirm=... on the button).
    click_status_button(page, "Cancel")
    page.wait_for_timeout(1500)

    # Confirm the native Odoo Dialog.
    for _ in range(3):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        m = modal.last
        confirm_btn = m.locator(
            ".modal-footer button.btn-primary:visible, "
            ".modal-footer button:has-text('Ok'):visible, "
            ".modal-footer button:has-text('Confirm'):visible, "
            ".modal-footer button:has-text('Yes'):visible"
        ).first
        if confirm_btn.count() > 0:
            confirm_btn.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
            continue
        break

    page.wait_for_timeout(800)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    _open_delivery(page)
    _cancel_and_confirm(page)


run_oracle(oracle)
