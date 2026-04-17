"""Oracle for hr.unarchive_employee_update_department.

Apply the Archived filter, open Avery Collins, unarchive via Action
menu, set Department to Engineering, save.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    schedule_activity,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    # Switch to list view for reliable row clicks
    list_switch = page.locator(
        ".o_switch_view.o_list:visible, "
        "button[data-tooltip='List']:visible, "
        ".o_cp_switch_buttons button:has-text('List')"
    ).first
    if list_switch.count() > 0:
        list_switch.click()
        _wait_no_loading(page)
        page.wait_for_timeout(500)

    # Open the search panel dropdown (has Filters/Group By/Favorites)
    toggler = page.locator(
        ".o_searchview_dropdown_toggler:visible"
    ).first
    toggler.click()
    page.wait_for_timeout(500)
    archived = page.locator(
        ".o_search_bar_menu .o_filter_menu .o_menu_item:has-text('Archived'), "
        ".o_search_bar_menu .dropdown-item:has-text('Archived'), "
        ".o-dropdown--menu:visible .o_menu_item:has-text('Archived')"
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

    click_tab(page, "Work")
    page.wait_for_timeout(500)
    set_many2one(page, "work_location_id", "Home")
    page.wait_for_timeout(500)

    set_many2one(page, "department_id", "Engineering")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    schedule_activity(
        page,
        activity_type="Call",
        summary="Complete reactivation checklist",
        due_date="05/21/2026",
    )
    page.wait_for_timeout(800)


run_oracle(oracle)
