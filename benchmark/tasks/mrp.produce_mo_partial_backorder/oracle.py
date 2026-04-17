"""Oracle for mrp.produce_mo_partial_backorder.

Open WH/MO/BENCH-PART-001, set quantity producing to 6, click Produce All,
then in the backorder dialog choose Create Backorder.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Open the target MO from the list.
    row = page.locator(".o_data_row td:has-text('BENCH-PART-001')").first
    row.click()
    _wait_for_ready(page)
    page.wait_for_timeout(1500)

    # Set Quantity Producing to 6. The field is qty_producing on mrp.production.
    qty_field = page.locator(
        "div[name='qty_producing'] input"
    ).first
    qty_field.click()
    qty_field.press("Control+A")
    qty_field.press("Meta+A")
    qty_field.fill("6")
    qty_field.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Click Produce All (button_mark_done).
    produce_btn = page.locator(
        "button[name='button_mark_done']:visible"
    )
    for i in range(produce_btn.count()):
        btn = produce_btn.nth(i)
        if btn.is_visible():
            txt = btn.inner_text()
            if "Produce All" in txt or "Mark as Done" in txt:
                btn.click()
                break
    else:
        if produce_btn.count() > 0 and produce_btn.first.is_visible():
            produce_btn.first.click()

    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # The backorder wizard. Find a visible modal and click the button
    # whose name is action_backorder (Create Backorder) — NOT the
    # action_generate_consumption_warning / no-backorder one.
    dialog = page.locator(".modal:visible")
    if dialog.count() > 0:
        # Try "Create Backorder" button by its text first.
        create_bo = dialog.last.locator(
            "button:has-text('Create Backorder'):visible"
        )
        if create_bo.count() > 0:
            create_bo.first.click()
        else:
            # Fallback: first .btn-primary in the dialog.
            pbtn = dialog.last.locator("button.btn-primary:visible").first
            if pbtn.count() > 0:
                pbtn.click()
        page.wait_for_timeout(2500)
        _wait_no_loading(page)

    # Handle any second dialog (consumption warning, etc.)
    dialog = page.locator(".modal:visible")
    if dialog.count() > 0:
        pbtn = dialog.last.locator("button.btn-primary:visible").first
        if pbtn.count() > 0:
            pbtn.click()
            page.wait_for_timeout(2000)
            _wait_no_loading(page)


run_oracle(oracle)
