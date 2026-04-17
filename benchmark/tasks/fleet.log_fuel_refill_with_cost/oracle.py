"""Oracle for fleet.log_fuel_refill_with_cost.

Open vehicle FUEL-9001, click Services stat button, create a new service
with the exact fields, save.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_stat_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/fleet")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Clear filters and switch to list.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break
    _wait_no_loading(page)
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)

    click_list_row(page, "FUEL-9001")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Click Services stat button.
    try:
        click_stat_button(page, "Services")
    except Exception:
        stat = page.locator("button.oe_stat_button:has-text('Services'):visible")
        if stat.count() > 0:
            stat.first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Click New.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    new_btn.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Service type — preseeded, select via normal many2one autocomplete.
    set_many2one(page, "service_type_id", "Refueling")
    page.wait_for_timeout(400)

    # Vendor — preseeded in res.partner.
    set_many2one(page, "vendor_id", "BP Express Holloway")

    # Amount.
    fill_field(page, "amount", "87.50")

    # Date.
    set_date(page, "date", "05/20/2026")

    # Notes / Description.
    notes = page.locator(".o_field_widget[name='description'] textarea:visible, .o_field_widget[name='notes'] textarea:visible")
    if notes.count() > 0:
        notes.first.click()
        notes.first.fill("42 L unleaded at £2.08/L")

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
