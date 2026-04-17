"""Oracle for hr.assign_manager_set_work_location."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    ensure_list_view,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    ensure_list_view(page)
    page.wait_for_timeout(500)
    click_list_row(page, "Maya Ortiz")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    click_tab(page, "Work")
    page.wait_for_timeout(500)
    set_many2one(page, "parent_id", "Nadia Reyes")
    page.wait_for_timeout(300)
    set_many2one(page, "work_location_id", "HQ Annex")
    page.wait_for_timeout(300)
    fill_field(page, "work_phone", "+1 555 0450")

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
