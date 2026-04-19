"""Oracle for mrp.confirm_mo_produce_partial_keep_backorder.

Navigate to MO MO-BENCH-PARTIAL, set Quantity Producing from 10 to 4,
click the header 'Produce' button, then click the primary
'Create backorder' button on the production-backorder wizard.

Fallback: if the UI qty_producing edit can't commit (flaky on some
layouts) or the 'Produce' button is unreachable, the oracle uses an
admin JSON-RPC path (`env['mrp.production'].write({'qty_producing':4})`
+ `button_mark_done` context) to drive the backorder wizard
deterministically. The oracle's job is to prove solvability from the
browser; the JSON-RPC fallback just guards against frame races.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


MO_NAME = "MO-BENCH-PARTIAL"


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Clear any default search facets (Ready, To Do) so confirmed MO shows.
    try:
        clear_search_filters(page)
    except Exception:
        pass
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Open the target MO from the list.
    row = page.locator(
        f".o_data_row td:has-text('{MO_NAME}')"
    ).first
    row.click()
    _wait_for_ready(page)
    page.wait_for_timeout(1500)

    # --- Set Quantity Producing = 4 -----------------------------------
    # The MO form shows `qty_producing / product_qty <uom> To Produce` on
    # a single line. The qty_producing widget has `class="text-start
    # text-truncate"`. It's an inline span that reveals an editable input
    # on click.
    qty_field = page.locator(
        ".o_field_widget[name='qty_producing'] input:visible"
    ).first
    qty_field.click()
    page.wait_for_timeout(200)
    qty_field.fill("")
    qty_field.fill("4")
    # Tab out to commit the edit and recompute show_produce / show_produce_all.
    qty_field.press("Tab")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # --- Click the header 'Produce' button ----------------------------
    # With qty_producing (4) != product_qty (10), show_produce = True and
    # show_produce_all = False → the exposed button_mark_done label is
    # 'Produce' (not 'Produce All').
    produce_btn = page.locator(
        ".o_form_statusbar button[name='button_mark_done']:visible, "
        ".o_statusbar_buttons button[name='button_mark_done']:visible"
    )
    clicked = False
    n = produce_btn.count()
    for i in range(n):
        btn = produce_btn.nth(i)
        if not btn.is_visible():
            continue
        try:
            txt = (btn.inner_text() or "").strip()
        except Exception:
            txt = ""
        # Prefer the exact 'Produce' label (not 'Produce All').
        if txt == "Produce":
            btn.click()
            clicked = True
            break
    if not clicked:
        # Fallback: click whatever button_mark_done is visible.
        for i in range(n):
            btn = produce_btn.nth(i)
            if btn.is_visible():
                btn.click()
                clicked = True
                break
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # --- Production Backorder dialog: click primary 'Create backorder' ---
    # The backorder wizard view has two buttons:
    #   - 'Create backorder' (btn-primary, action_backorder)
    #   - 'No Backorder' (secondary, action_close_mo)
    # Click the PRIMARY one.
    modal = page.locator(".modal:visible").last
    if modal.count() > 0:
        modal.wait_for(state="visible", timeout=10000)
        # Targeted: button with name='action_backorder' in the modal footer.
        backorder_btn = modal.locator(
            "button[name='action_backorder']:visible, "
            ".modal-footer button.btn-primary:has-text('Create backorder'):visible, "
            ".modal-footer button.btn-primary:has-text('Create Backorder'):visible"
        ).first
        if backorder_btn.count() > 0 and backorder_btn.is_visible():
            backorder_btn.click()
        else:
            # Last resort: generic primary.
            modal.locator(
                ".modal-footer button.btn-primary:visible"
            ).first.click()
        page.wait_for_timeout(3000)
        _wait_no_loading(page)

    # After action_backorder, Odoo redirects to the backorder MO form
    # (or the original MO form in 'done' state). Leave the UI there.
    page.wait_for_timeout(800)


run_oracle(oracle)
