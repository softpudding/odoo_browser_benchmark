"""Oracle for hr.schedule_employee_activity.

Open employee Sofia Chen, schedule a Call activity with due date May 10, 2026
and summary "Annual review discussion".
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    set_date,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    # Find and open Sofia Chen
    click_list_row(page, "Sofia Chen")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Click Schedule Activity button
    page.get_by_role("button", name="Schedule Activity").click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Set Activity Type to Call
    page.get_by_label("Activity Type").click()
    page.get_by_role("option", name="Call").click()
    page.wait_for_timeout(500)

    # Set Due Date
    set_date(page, "Due Date", "05/10/2026")
    page.wait_for_timeout(500)

    # Set Summary
    page.get_by_label("Summary").fill("Annual review discussion")
    page.wait_for_timeout(500)

    # Click Schedule Activity
    page.get_by_role("button", name="Schedule Activity").last.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)