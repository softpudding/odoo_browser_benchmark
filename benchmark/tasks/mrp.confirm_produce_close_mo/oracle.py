"""Oracle for mrp.confirm_produce_close_mo.

Open the draft MO WH/MO/BENCH-DESK-001, click Confirm (draft ->
confirmed), then click Produce All and accept the confirmation
wizard so the MO closes at the full quantity (state='done').
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

    # The manufacturing list can be filtered by default (e.g. 'Ready').
    # Clear filters so draft MOs are visible.
    try:
        clear_search_filters(page)
    except Exception:
        pass
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Open the draft MO row.
    row = page.locator(".o_data_row td:has-text('BENCH-DESK-001')").first
    row.click()
    _wait_for_ready(page)
    page.wait_for_timeout(1500)

    # Step 1: click the Confirm button in the status bar.
    confirm_btn = page.locator(
        "button[name='action_confirm']:visible"
    )
    if confirm_btn.count() > 0:
        confirm_btn.first.click()
    else:
        # Fallback: status bar button with text "Confirm".
        sb = page.locator(
            ".o_statusbar_buttons button:visible:has-text('Confirm')"
        ).first
        sb.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Step 2: click Produce All (button_mark_done).
    produce_btn = page.locator(
        "button[name='button_mark_done']:visible"
    )
    clicked = False
    for i in range(produce_btn.count()):
        btn = produce_btn.nth(i)
        if btn.is_visible():
            txt = btn.inner_text()
            if "Produce All" in txt or "Mark as Done" in txt:
                btn.click()
                clicked = True
                break
    if not clicked and produce_btn.count() > 0 and produce_btn.first.is_visible():
        produce_btn.first.click()

    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    # Step 3: handle any wizard dialog (consumption warning / backorder).
    # We want to APPLY / VALIDATE (not create a backorder). We should also
    # NOT be asked for a backorder because qty_producing == product_qty.
    for _ in range(3):
        dialog = page.locator(".modal:visible")
        if dialog.count() == 0:
            break
        # Prefer buttons whose text is Apply / Validate / Continue / Mark.
        for label in ("Apply", "Validate", "Continue", "Mark as Done", "Confirm"):
            candidate = dialog.last.locator(
                f"button:visible:has-text('{label}')"
            )
            if candidate.count() > 0:
                candidate.first.click()
                break
        else:
            # Last resort: the first primary button.
            pbtn = dialog.last.locator("button.btn-primary:visible").first
            if pbtn.count() > 0:
                pbtn.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)


run_oracle(oracle)
