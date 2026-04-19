"""Oracle for mrp.unbuild_product_back_to_components.

Navigate to Unbuild Orders, click New, set product=Bench Assembly
(BoM auto-fills), Quantity=2, leave MO empty + locations at defaults,
click Unbuild / Validate in the statusbar.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    set_many2one,
    _wait_no_loading,
)


FINISHED = "Bench Assembly"


def oracle(page):
    login(page)
    # Direct action URL for unbuild orders avoids menu-path fragility.
    navigate(page, "/odoo/action-mrp.mrp_unbuild")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Clear any default filters (e.g. "Draft") so the list / new-button
    # state is clean.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break

    # --- Click New -----------------------------------------------------
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    new_btn.first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # --- Product = Bench Assembly --------------------------------------
    # BoM should auto-fill from the onchange.
    set_many2one(page, "product_id", FINISHED)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # --- Quantity = 2 --------------------------------------------------
    qty_input = page.locator(
        ".o_field_widget[name='product_qty'] input:visible"
    ).first
    qty_input.click()
    qty_input.fill("")
    qty_input.fill("2")
    page.keyboard.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # --- Click Unbuild / Validate in the statusbar ---------------------
    unbuild_btn = page.locator(
        ".o_form_statusbar button[name='action_validate']:visible, "
        ".o_form_statusbar button[name='action_unbuild']:visible, "
        ".o_form_statusbar button:has-text('Unbuild'):visible"
    )
    unbuild_btn.first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # --- Handle any confirmation modal (consumption warning etc.) ------
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
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
