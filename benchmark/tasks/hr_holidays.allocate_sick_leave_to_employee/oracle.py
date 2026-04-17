"""Oracle for hr_holidays.allocate_sick_leave_to_employee."""

from benchmark.oracle_helpers import (
    _wait_no_loading,
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
)


def _click_new(page):
    new_btn = page.locator(
        "button.o_list_button_add:visible, button.o-kanban-button-new:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    if new_btn.count() > 0:
        new_btn.first.click()
    else:
        page.locator("button:has-text('New'):visible").first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/time-off")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Open Management > Allocations via the app menu
    # Click on "Management" top menu dropdown
    mgmt = page.locator(
        "nav.o_main_navbar button:has-text('Management'), "
        "nav.o_main_navbar .o_nav_entry:has-text('Management'), "
        ".o_menu_sections button:has-text('Management'), "
        ".o_menu_sections a:has-text('Management')"
    )
    if mgmt.count() > 0:
        mgmt.first.click()
        page.wait_for_timeout(600)
        alloc_item = page.locator(
            ".o-dropdown--menu .dropdown-item:has-text('Allocations'), "
            ".o_menu_sections a:has-text('Allocations'), "
            ".dropdown-menu a:has-text('Allocations')"
        )
        alloc_item.first.click()
    else:
        # Fallback: navigate via Management > Allocations link directly
        page.locator("a:has-text('Allocations'):visible").first.click()
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    _click_new(page)

    # Fill employee
    set_many2one(page, "employee_id", "Benchmark Allocatee")
    page.wait_for_timeout(600)

    # Fill time off type
    set_many2one(page, "holiday_status_id", "Sick Time Off")
    page.wait_for_timeout(600)

    # Fill duration (number_of_days_display is the editable display field)
    # Try the display field first, then fall back to number_of_days.
    for field_name in ("number_of_days_display", "number_of_days"):
        widget = page.locator(
            f".o_field_widget[name='{field_name}'] input"
        )
        if widget.count() > 0 and widget.first.is_visible():
            widget.first.click()
            widget.first.fill("")
            widget.first.type("15")
            widget.first.press("Tab")
            page.wait_for_timeout(400)
            break

    # Save the form
    save_form(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Click Validate (or Approve) -- backend method name is action_approve
    validate_btn = page.locator(
        "button[name='action_approve']:visible, "
        "button:has-text('Validate'):visible, "
        "button:has-text('Approve'):visible"
    )
    if validate_btn.count() > 0:
        validate_btn.first.click()
        page.wait_for_load_state("load")
        _wait_no_loading(page)
        page.wait_for_timeout(1500)


run_oracle(oracle)
