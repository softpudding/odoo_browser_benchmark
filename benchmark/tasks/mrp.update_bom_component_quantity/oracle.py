"""Oracle for mrp.update_bom_component_quantity."""

from benchmark.oracle_helpers import (
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    save_form,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)

    # Navigate: Products > Bills of Materials
    page.locator('.o_menu_sections .dropdown-toggle:has-text("Products")').first.click()
    page.wait_for_timeout(500)
    page.locator('.dropdown-menu:visible .dropdown-item:has-text("Bills of Materials")').first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    ensure_list_view(page)
    click_list_row(page, "BOM-BENCH-MIXER")
    page.wait_for_timeout(1000)

    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    for i in range(rows.count()):
        if "Aluminum Housing" in rows.nth(i).inner_text():
            set_o2m_field(page, i, "product_qty", "3")
            break

    save_form(page)


run_oracle(oracle)
