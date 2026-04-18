"""Oracle for hr.create_department_assign_manager_three_employees.

1. Navigate to Departments, create 'Bench Engineering' with manager Mike Manager.
2. Navigate to Employees and reassign each of the three engineers'
   department to Bench Engineering.
"""

from benchmark.oracle_helpers import (
    click_create,
    click_list_row,
    ensure_list_view,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


ENGINEERS = ["Eng One", "Eng Two", "Eng Three"]


def _open_employee_form(page, name):
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)
    ensure_list_view(page)
    page.wait_for_timeout(500)
    click_list_row(page, name)
    _wait_for_ready(page)
    page.wait_for_timeout(500)


def oracle(page):
    login(page)

    # ---- Step 1: Create the new department ----
    navigate(page, "/odoo/departments")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    click_create(page)
    page.wait_for_timeout(800)
    fill_field(page, "name", "Bench Engineering")
    page.wait_for_timeout(400)
    set_many2one(page, "manager_id", "Mike Manager")
    page.wait_for_timeout(400)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # ---- Step 2: Reassign each engineer's department ----
    for name in ENGINEERS:
        _open_employee_form(page, name)
        set_many2one(page, "department_id", "Bench Engineering")
        page.wait_for_timeout(400)
        save_form(page)
        page.wait_for_timeout(800)
        _wait_no_loading(page)


run_oracle(oracle)
