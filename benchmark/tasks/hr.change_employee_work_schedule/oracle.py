"""Oracle for hr.change_employee_work_schedule.

Open Employees > 'Bench Sched Me', switch to the Payroll tab, change
the Working Hours many2one (``resource_calendar_id``) from 'Standard
40 hours/week' to 'Part Time 20h' via autocomplete, and save.

Note: ``resource_calendar_id`` lives under the Payroll tab's Schedule
section (``addons/hr/views/hr_employee_views.xml:353``, grouped by
``hr.group_hr_manager`` — admin has access).
"""

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
)

EMPLOYEE_NAME = "Bench Sched Me"
PART_TIME_CALENDAR_NAME = "Part Time 20h"


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Open the seeded employee from the kanban/list view.
    click_list_row(page, EMPLOYEE_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Switch to Payroll tab. The resource_calendar_id m2o ("Working
    # Hours") is rendered on this tab under the Schedule separator.
    click_tab(page, "Payroll")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Change the Working Hours m2o to 'Part Time 20h' via autocomplete.
    set_many2one(page, "resource_calendar_id", PART_TIME_CALENDAR_NAME)
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
