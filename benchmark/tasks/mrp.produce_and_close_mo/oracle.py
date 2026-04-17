"""Oracle for mrp.produce_and_close_mo.

Navigate to Manufacturing Orders, open WH/MO/BENCH-001,
click Produce All to complete the MO.
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

    # The default view should be list. Click the MO row.
    # Use a broader selector to find the row
    row = page.locator(
        ".o_data_row td:has-text('BENCH-001')"
    ).first
    row.click()
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Now we should be on the MO form.
    # Click "Produce All" — try by button name first
    produce_btn = page.locator(
        "button[name='button_mark_done']:visible"
    )
    # There may be multiple buttons with this name (with/without components)
    # Filter to the one that says "Produce All"
    for i in range(produce_btn.count()):
        btn = produce_btn.nth(i)
        if btn.is_visible():
            txt = btn.inner_text()
            if "Produce All" in txt:
                btn.click()
                break
    else:
        # Fallback: click any visible button_mark_done
        if produce_btn.first.is_visible():
            produce_btn.first.click()

    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    # Handle any wizard/dialog that might appear
    dialog = page.locator(".modal:visible")
    if dialog.count() > 0:
        confirm_btn = dialog.last.locator(
            "button.btn-primary:visible"
        ).first
        if confirm_btn.count() > 0:
            confirm_btn.click()
            page.wait_for_timeout(2000)
            _wait_no_loading(page)


run_oracle(oracle)
