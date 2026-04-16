"""Oracle for project.add_task_subtask.

Open task Design Landing Page Mockup, go to Subtasks tab, add subtask
Create Wireframes, and save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    click_tab,
    click_add_a_line,
    set_o2m_field,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # Open the project
    click_list_row(page, "Omega Platform Launch")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Find and open the task
    click_list_row(page, "Design Landing Page Mockup")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Go to Subtasks tab
    click_tab(page, "Subtasks")
    page.wait_for_timeout(500)

    # Add a new subtask
    click_add_a_line(page)
    page.wait_for_timeout(500)

    # Set the subtask name
    set_o2m_field(page, 0, "name", "Create Wireframes")

    # Click Save
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
