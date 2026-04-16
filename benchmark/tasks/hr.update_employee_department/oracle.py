"""Oracle for hr.update_employee_department.

Find employee Sofia Chen, change Department to Engineering, and click Save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    set_many2one,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    # Find and open Sofia Chen
    click_list_row(page, "Sofia Chen")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Change Department to Engineering
    set_many2one(page, "department_id", "Engineering")

    # Click Save
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
