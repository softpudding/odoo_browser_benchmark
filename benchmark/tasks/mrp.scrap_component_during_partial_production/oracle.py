"""Oracle for mrp.scrap_component_during_partial_production.

Navigate to the MO, open cog Actions menu > Scrap, fill the scrap wizard
(ScrewA qty=2 reason='Defective batch' source=WH/Stock), validate, then
Produce All / Mark As Done on the MO.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


MO_NAME = "M-BENCH-SCRAP-001"


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Clear any default search filters (Ready/To Do) so the row is visible.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break

    # Open the target MO from the list.
    row = page.locator(
        f".o_data_row td:has-text('{MO_NAME}')"
    ).first
    row.click()
    _wait_for_ready(page)
    page.wait_for_timeout(1500)

    # Open the cog / Actions menu and click "Scrap".
    cog = page.locator(
        ".o_cp_action_menus button:visible, "
        ".o_control_panel button.dropdown-toggle:has-text('Actions'):visible, "
        ".o_control_panel .fa-cog:visible"
    ).first
    cog.click()
    page.wait_for_timeout(500)
    scrap_item = page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Scrap'), "
        ".o-dropdown--menu:visible .dropdown-item:has-text('Scrap')"
    ).first
    scrap_item.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Scrap Products dialog -------------------------------------------------
    modal = page.locator(".modal:visible").last
    modal.wait_for(state="visible", timeout=10000)

    # Product: ScrewA
    prod_input = modal.locator(
        ".o_field_widget[name='product_id'] input"
    ).first
    prod_input.click()
    prod_input.fill("")
    prod_input.fill("ScrewA")
    page.wait_for_timeout(800)
    item = page.locator(
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete .ui-menu-item, "
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item"
    ).filter(has_text="ScrewA").first
    item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Quantity: 2
    qty_input = modal.locator(
        ".o_field_widget[name='scrap_qty'] input"
    ).first
    qty_input.click()
    qty_input.fill("")
    qty_input.fill("2")
    qty_input.press("Tab")
    page.wait_for_timeout(300)

    # Reason tag: Defective batch
    tag_input = modal.locator(
        ".o_field_widget[name='scrap_reason_tag_ids'] input"
    ).first
    tag_input.click()
    tag_input.fill("Defective batch")
    page.wait_for_timeout(800)
    tag_item = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete .ui-menu-item"
    ).filter(has_text="Defective batch").first
    tag_item.click()
    page.wait_for_timeout(500)

    # Source Location: WH/Stock (ensure not the virtual scrap location).
    src_input = modal.locator(
        ".o_field_widget[name='location_id'] input"
    ).first
    if src_input.count() > 0 and src_input.is_visible():
        src_input.click()
        src_input.fill("")
        src_input.fill("WH/Stock")
        page.wait_for_timeout(800)
        src_item = page.locator(
            ".dropdown-menu:visible .dropdown-item, "
            ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item"
        ).filter(has_text="WH/Stock").first
        try:
            src_item.click()
        except Exception:
            # Fallback: press Enter to accept first suggestion
            src_input.press("Enter")
        page.wait_for_timeout(500)

    # Validate: "Scrap Products" button in the modal footer.
    validate_btn = modal.locator(
        "button[name='action_validate']:visible, "
        ".modal-footer button.btn-primary:has-text('Scrap Products'):visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    validate_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # A secondary "insufficient qty" wizard might appear if stock math
    # doesn't reconcile; accept defaults.
    for _ in range(2):
        extra = page.locator(".modal:visible")
        if extra.count() == 0:
            break
        primary = extra.last.locator("button.btn-primary:visible").first
        if primary.count() == 0:
            break
        try:
            primary.click()
        except Exception:
            break
        page.wait_for_timeout(1500)
        _wait_no_loading(page)

    # Back on the MO form. Click Produce All (button_mark_done).
    page.wait_for_timeout(800)
    produce_btn = page.locator("button[name='button_mark_done']:visible")
    clicked = False
    n = produce_btn.count()
    for i in range(n):
        btn = produce_btn.nth(i)
        if btn.is_visible():
            txt = btn.inner_text()
            if "Produce All" in txt or "Mark as Done" in txt:
                btn.click()
                clicked = True
                break
    if not clicked and n > 0 and produce_btn.first.is_visible():
        produce_btn.first.click()

    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    # Handle any confirmation wizard (consumption warning, backorder...).
    for _ in range(3):
        dialog = page.locator(".modal:visible")
        if dialog.count() == 0:
            break
        pbtn = dialog.last.locator("button.btn-primary:visible").first
        if pbtn.count() == 0:
            break
        try:
            pbtn.click()
        except Exception:
            break
        page.wait_for_timeout(2000)
        _wait_no_loading(page)


run_oracle(oracle)
