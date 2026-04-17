"""Oracle for hr_holidays.request_half_day_morning.

Open Time Off, create a new request with Paid Time Off, half day morning,
2026-06-15, description 'Doctor appointment'. Leave in To Approve state.
"""

from benchmark.oracle_helpers import (
    fill_text_field,
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
    navigate(page, "/odoo/time-off")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Click New button.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible, "
        "button:has-text('New Time Off'):visible"
    )
    new_btn.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Leave type.
    set_many2one(page, "holiday_status_id", "Paid Time Off")
    page.wait_for_timeout(400)

    # Toggle Half Day using the boolean toggle widget. Use .check() on the
    # underlying checkbox — Playwright's check() handles label-associated
    # checkboxes even when the visible UI is a switch.
    try:
        cb = page.locator("input[name='request_unit_half']").first
        cb.check(force=True)
    except Exception:
        # Fallback: click the label.
        lab = page.locator("label:has-text('Half Day'):visible")
        if lab.count() > 0:
            lab.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Set the single date field using the robust set_date helper.
    set_date(page, "request_date_from", "06/15/2026")

    # Morning ('am') is the default when Half Day is toggled on — no action
    # needed; but attempt a best-effort select if the control is a plain
    # <select> and the current value is 'pm'.
    try:
        select = page.locator("div[name='request_date_from_period'] select:visible")
        if select.count() > 0:
            select.first.select_option("am")
    except Exception:
        pass

    # Description (name) — textarea on the leave form.
    fill_text_field(page, "name", "Doctor appointment")

    save_form(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
