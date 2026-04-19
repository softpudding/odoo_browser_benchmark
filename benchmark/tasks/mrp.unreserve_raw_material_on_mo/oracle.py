"""Oracle for mrp.unreserve_raw_material_on_mo.

Navigate to MO MO-BENCH-UNRES and click the header 'Unreserve' button
(name='do_unreserve'). No wizard — a single click commits the change.

The button is visible because unreserve_visible=True (MO is confirmed
with reserved move lines and no picked qty). Clicking it cascades
through `mrp.production.do_unreserve` → `stock.move._do_unreserve`,
which unlinks move_line_ids and recomputes the raw move's state from
'assigned' back to 'confirmed'.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


MO_NAME = "MO-BENCH-UNRES"


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Clear default search facets (Ready, To Do) so confirmed MO shows.
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

    # --- Click the header 'Unreserve' button --------------------------
    # View declaration:
    #   <button name="do_unreserve" type="object" string="Unreserve"
    #           invisible="not unreserve_visible" data-hotkey="w"/>
    # Prefer exact name='do_unreserve' selector; fall back to string
    # match across statusbar buttons.
    unreserve_btn = page.locator(
        ".o_form_statusbar button[name='do_unreserve']:visible, "
        ".o_statusbar_buttons button[name='do_unreserve']:visible"
    ).first

    clicked = False
    try:
        if unreserve_btn.count() > 0 and unreserve_btn.is_visible():
            unreserve_btn.click()
            clicked = True
    except Exception:
        pass

    if not clicked:
        # Fallback: search visible statusbar buttons for label "Unreserve".
        candidates = page.locator(
            ".o_form_statusbar button:visible, "
            ".o_statusbar_buttons button:visible"
        )
        n = candidates.count()
        for i in range(n):
            btn = candidates.nth(i)
            if not btn.is_visible():
                continue
            try:
                txt = (btn.inner_text() or "").strip()
            except Exception:
                txt = ""
            if txt == "Unreserve":
                btn.click()
                clicked = True
                break

    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # After do_unreserve the button disappears (unreserve_visible flips
    # to False because move_line_ids are unlinked). Leave the form as-is.
    page.wait_for_timeout(500)


run_oracle(oracle)
