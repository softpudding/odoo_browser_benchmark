"""Oracle for hr.unarchive_employee_update_department.

Apply the Archived filter, open Avery Collins, unarchive via Action
menu, set Department to Engineering, save.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    # Apply Archived filter via Filters dropdown
    filters_btn = page.locator(
        ".o_searchview_dropdown_toggler:has-text('Filters'):visible, "
        ".o_search_panel .o_filter_toggle:visible, "
        ".o_control_panel button:has-text('Filters'):visible"
    ).first
    filters_btn.click()
    page.wait_for_timeout(500)
    archived = page.locator(
        ".o-dropdown--menu:visible .dropdown-item:has-text('Archived'), "
        ".dropdown-menu:visible .dropdown-item:has-text('Archived')"
    ).first
    archived.click()
    page.wait_for_timeout(500)
    # Close the filter dropdown
    page.keyboard.press("Escape")
    _wait_no_loading(page)

    click_list_row(page, "Avery Collins")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Open Actions menu and click Unarchive
    cog = page.locator(
        ".o_cp_action_menus button:visible, "
        ".o_control_panel button.dropdown-toggle:has-text('Actions'):visible, "
        ".o_control_panel .fa-cog:visible"
    ).first
    cog.click()
    page.wait_for_timeout(500)
    unarchive = page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Unarchive'), "
        ".o-dropdown--menu:visible .dropdown-item:has-text('Unarchive')"
    ).first
    unarchive.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    set_many2one(page, "department_id", "Engineering")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
