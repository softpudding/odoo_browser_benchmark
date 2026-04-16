"""Oracle for hr.update_work_information.

Find employee "Sofia Chen", update Work Location to "Home" (Work tab) and
Timezone to "America/New_York" (Settings tab), then update Certificate Level
to "Master" (Personal tab). Save.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
)


def _select_menu(page, field_name, label):
    """Select a value from Odoo 19 SelectMenu / searchable selection."""
    widget = page.locator(f".o_field_widget[name='{field_name}']").first
    # Try a plain <select> first
    sel = widget.locator("select")
    if sel.count() > 0 and sel.first.is_visible():
        sel.first.select_option(label=label)
        page.wait_for_timeout(300)
        return
    # Otherwise: searchable dropdown (input)
    inp = widget.locator("input")
    if inp.count() > 0 and inp.first.is_visible():
        inp.first.click()
        page.wait_for_timeout(300)
        inp.first.fill("")
        inp.first.fill(label)
        page.wait_for_timeout(600)
    else:
        btn = widget.locator("button, .dropdown-toggle").first
        btn.click()
        page.wait_for_timeout(500)
    items = page.locator(
        ".dropdown-menu:visible .o-dropdown-item, "
        ".o_select_menu_menu:visible .o_select_menu_item, "
        ".dropdown-menu:visible .dropdown-item"
    )
    item = items.filter(has_text=label).first
    if item.count() > 0:
        item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    # Find and open Sofia Chen
    click_list_row(page, "Sofia Chen")
    page.wait_for_timeout(500)

    # Work tab — work_location_id
    click_tab(page, "Work")
    page.wait_for_timeout(500)
    set_many2one(page, "work_location_id", "Home")
    page.wait_for_timeout(500)

    # Settings tab — tz
    click_tab(page, "Settings")
    page.wait_for_timeout(500)
    _select_menu(page, "tz", "America/New_York")
    page.wait_for_timeout(500)

    # Personal tab — certificate
    click_tab(page, "Personal")
    page.wait_for_timeout(500)
    _select_menu(page, "certificate", "Master")
    page.wait_for_timeout(500)

    # Save
    save_form(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
