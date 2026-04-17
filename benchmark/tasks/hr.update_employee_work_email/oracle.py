"""Oracle for hr.update_employee_work_email."""

from benchmark.oracle_helpers import (
    fill_field,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
    ensure_list_view,
    search_for,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    ensure_list_view(page)
    page.wait_for_timeout(500)
    search_for(page, "Lena Ortiz")
    page.wait_for_timeout(500)

    # Open the first matching row
    row = page.locator(".o_list_view .o_data_row").first
    row.click()
    page.wait_for_timeout(400)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    fill_field(page, "work_email", "lena.ortiz@ops.example.com")
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
