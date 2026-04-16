"""Oracle for hr.update_work_location_schedule_activity."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    schedule_activity,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    click_list_row(page, "Avery Collins")
    page.wait_for_timeout(800)

    fill_field(page, "work_phone", "+1 415 555 0188")
    page.wait_for_timeout(400)
    click_tab(page, "Work")
    page.wait_for_timeout(500)
    set_many2one(page, "work_location_id", "Home")
    page.wait_for_timeout(500)
    save_form(page)
    page.wait_for_timeout(700)

    schedule_activity(
        page,
        activity_type="Call",
        summary="Confirm home office setup",
        due_date="05/19/2026",
    )
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
