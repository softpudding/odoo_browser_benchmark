"""Oracle for project.set_task_deadline.

Open task Design Landing Page Mockup, change deadline to May 20, 2026, save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    set_date,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # Open the project
    click_list_row(page, "Omega Platform Launch")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Find and open the task
    click_list_row(page, "Design Landing Page Mockup")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Change the deadline
    set_date(page, "date_deadline", "05/20/2026")
    page.wait_for_timeout(500)

    # Click Save
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)