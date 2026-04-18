"""Oracle for inventory.run_replenishment_from_dashboard.

Navigate to the Inventory > Operations > Replenishment dashboard, find the row
for "Bench Reorder Widget", and click the Order button (named action_replenish
in the list view) to launch a draft purchase order.
"""

import os
import sys
import traceback

from benchmark.oracle_helpers import (
    login,
    navigate,
    odoo_browser,
    _wait_no_loading,
    _wait_for_ready,
)

PRODUCT_NAME = "Bench Reorder Widget"


def oracle(page):
    login(page)
    # The Replenishment server-action has path="replenishment".
    navigate(page, "/odoo/replenishment")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Search for the target product row (the dashboard may include other lines).
    search_input = page.locator(".o_searchview_input").first
    search_input.fill(PRODUCT_NAME)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    row = page.locator(f".o_data_row:has-text('{PRODUCT_NAME}')").first
    row.wait_for(state="visible", timeout=15000)

    # Click the Order button on that row. The list view defines this as a
    # button[name='action_replenish'] with class 'o_replenish_buttons'.
    order_btn = row.locator(
        "button[name='action_replenish'].o_replenish_buttons, "
        "button[name='action_replenish']"
    ).first
    order_btn.wait_for(state="visible", timeout=10000)
    order_btn.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # If a confirmation modal/wizard opens (e.g., quantity prompt), confirm it.
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Confirm'), "
            "button:has-text('Order'), "
            "button:has-text('Apply'), "
            "button:has-text('Ok'), "
            "button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


def main():
    with odoo_browser() as page:
        try:
            oracle(page)
            print("Oracle: PASS")
            sys.exit(0)
        except Exception as exc:
            print(f"Oracle: FAIL - {exc}")
            traceback.print_exc()
            debug_path = os.environ.get("BENCHMARK_ORACLE_DEBUG")
            if debug_path:
                try:
                    page.screenshot(path=debug_path, full_page=True)
                    print(f"Oracle screenshot written to {debug_path}")
                except Exception:
                    pass
            sys.exit(1)


if __name__ == "__main__":
    main()
