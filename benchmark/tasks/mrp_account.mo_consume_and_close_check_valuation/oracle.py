"""Oracle for mrp_account.mo_consume_and_close_check_valuation.

Open the confirmed MO MO-BENCH-VAL and close it via Produce All /
Mark as Done (qty_producing == product_qty so no backorder wizard).
The oracle ends on the MO form in Done state; state diff + check.py
verifies the stock.move valuation rollup.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
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

    # Clear default filters (Ready, etc.) so confirmed MO is visible.
    try:
        clear_search_filters(page)
    except Exception:
        pass
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Open the MO.
    row = page.locator(".o_data_row td:has-text('MO-BENCH-VAL')").first
    row.click()
    _wait_for_ready(page)
    page.wait_for_timeout(1500)

    # --- Click Produce (pre_button_mark_done) if it's exposed ---
    produce_btn = page.locator(
        "button[name='pre_button_mark_done']:visible"
    )
    if produce_btn.count() > 0 and produce_btn.first.is_visible():
        produce_btn.first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)

    # --- Click Mark as Done / Produce All ---
    mark_done = page.locator(
        "button[name='button_mark_done']:visible"
    )
    clicked = False
    for i in range(mark_done.count()):
        btn = mark_done.nth(i)
        if btn.is_visible():
            txt = btn.inner_text()
            if (
                "Mark as Done" in txt
                or "Produce All" in txt
                or "Mark As Done" in txt
            ):
                btn.click()
                clicked = True
                break
    if not clicked and mark_done.count() > 0 and mark_done.first.is_visible():
        mark_done.first.click()
    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    # Accept any confirmation / consumption / backorder dialog.
    for _ in range(3):
        dialog = page.locator(".modal:visible")
        if dialog.count() == 0:
            break
        for label in (
            "Apply",
            "Validate",
            "Continue",
            "Mark as Done",
            "Confirm",
            "Ok",
        ):
            candidate = dialog.last.locator(
                f"button:visible:has-text('{label}')"
            )
            if candidate.count() > 0:
                candidate.first.click()
                break
        else:
            pbtn = dialog.last.locator("button.btn-primary:visible").first
            if pbtn.count() > 0:
                pbtn.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)


run_oracle(oracle)
