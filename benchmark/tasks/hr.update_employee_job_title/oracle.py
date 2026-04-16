"""Oracle for hr.update_employee_job_title."""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
    save_form,
    set_many2one,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    click_list_row(page, "Daniel Ortiz")
    _wait_for_ready(page)

    set_many2one(page, "job_id", "Operations Specialist")
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
