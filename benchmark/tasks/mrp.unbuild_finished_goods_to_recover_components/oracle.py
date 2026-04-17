"""Oracle for mrp.unbuild_finished_goods_to_recover_components.

Navigate to Unbuild Orders, click New, pick the target MO, confirm qty=3,
click Unbuild/Validate.
"""

from benchmark.oracle_helpers import (
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    # Direct action URL for unbuild orders.
    navigate(page, "/odoo/action-mrp.mrp_unbuild")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Clear filters.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break

    # Click New.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    new_btn.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Select MO (mo_id).
    set_many2one(page, "mo_id", "WH/MO/UNBLD-001")
    page.wait_for_timeout(600)

    # Set quantity = 3 (should default, but ensure).
    qty = page.locator(".o_field_widget[name='product_qty'] input:visible")
    if qty.count() > 0:
        qty.first.click()
        qty.first.fill("")
        qty.first.fill("3")
        page.keyboard.press("Tab")
        page.wait_for_timeout(300)

    save_form(page)
    page.wait_for_timeout(800)

    # Click Unbuild / Validate statusbar button.
    unbuild_btn = page.locator(
        ".o_form_statusbar button[name='action_validate']:visible, "
        ".o_form_statusbar button[name='action_unbuild']:visible, "
        ".o_form_statusbar button:has-text('Unbuild'):visible"
    )
    unbuild_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
