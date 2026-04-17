"""Oracle for hr_holidays.allocate_sick_leave_to_employee.

Navigate to Time Off, open Management > Allocations, create a new
allocation for Marc Demo / Sick Time Off / 15 days, save, then approve.
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

    # Go to Time Off root and click through menus to reach Allocations.
    navigate(page, "/odoo/time-off")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Open Management menu in the navbar.
    # The navbar menus in Odoo 19 are rendered as dropdowns with
    # data-section/labels. Try clicking the Management menu by text.
    mgmt = page.locator(
        ".o_menu_sections button:has-text('Management'):visible, "
        ".o_navbar_apps_menu_entry:has-text('Management'):visible, "
        "a.dropdown-toggle:has-text('Management'):visible"
    )
    if mgmt.count() > 0:
        mgmt.first.click()
        page.wait_for_timeout(500)
        # Click Allocations inside the Management submenu.
        alloc = page.locator(
            ".o-dropdown--menu a:has-text('Allocations'):visible, "
            ".dropdown-menu a:has-text('Allocations'):visible"
        )
        if alloc.count() > 0:
            alloc.first.click()
        else:
            # Fallback: direct URL to the allocations approve action.
            navigate(
                page,
                "/odoo/action-hr_holidays.hr_leave_allocation_action_approve_department",
            )
    else:
        navigate(
            page,
            "/odoo/action-hr_holidays.hr_leave_allocation_action_approve_department",
        )
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

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
    _wait_no_loading(page)

    # Click New.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    new_btn.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Fill in the allocation form.
    fill_field(page, "name", "2026 Sick leave pool")
    try:
        set_many2one(page, "employee_id", "Marc Demo")
    except Exception:
        pass
    set_many2one(page, "holiday_status_id", "Sick Time Off")

    # Set number of days (field may be number_of_days_display).
    days_input = page.locator(
        "div.o_field_widget[name='number_of_days_display'] input:visible, "
        "div.o_field_widget[name='number_of_days'] input:visible"
    )
    if days_input.count() > 0:
        days_input.first.fill("15")
        page.wait_for_timeout(300)

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Approve.
    approve_btn = page.locator(
        ".o_form_statusbar button[name='action_approve']:visible, "
        ".o_form_statusbar button[name='action_validate']:visible"
    )
    if approve_btn.count() > 0:
        approve_btn.first.click()
    else:
        btn = page.locator(
            "button:has-text('Approve'):visible, "
            "button:has-text('Validate'):visible"
        )
        if btn.count() > 0:
            btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
