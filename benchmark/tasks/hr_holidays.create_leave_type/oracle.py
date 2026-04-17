"""Oracle for hr_holidays.create_leave_type."""

from benchmark.oracle_helpers import (
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_selection,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    # Leave type config view.
    navigate(page, "/odoo/action-hr_holidays.open_view_holiday_status")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    fill_field(page, "name", "Conference Attendance")

    # Select "By Employee's Approver" on leave_validation_type radio
    # (backend value 'manager').
    try:
        set_selection(page, "leave_validation_type", "By Employee's Approver")
    except Exception:
        lab = page.locator(
            "label:has-text(\"By Employee's Approver\"):visible, "
            "input[type='radio'][value='manager']:visible"
        ).first
        try:
            lab.click(force=True)
        except Exception:
            pass

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
