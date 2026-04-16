"""Oracle for hr.update_work_information.

Find employee "Sofia Chen", update Work Location to "Home" and Timezone
to "America/New_York" in Work Information tab, then update Certificate
Level to "Master" in Private Information tab. Save.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_selection,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    # Find and open Sofia Chen
    click_list_row(page, "Sofia Chen")
    page.wait_for_timeout(500)

    # Go to Work Information tab
    click_tab(page, "Work Information")
    page.wait_for_timeout(500)

    # Set work location to Home
    set_many2one(page, "work_location_id", "Home")
    page.wait_for_timeout(500)

    # Set timezone — this is a selection field in Odoo
    set_selection(page, "tz", "America/New_York")
    page.wait_for_timeout(500)

    # Go to Private Information tab
    click_tab(page, "Private Information")
    page.wait_for_timeout(500)

    # Set certificate level to Master
    set_selection(page, "certificate", "Master")
    page.wait_for_timeout(500)

    # Save
    save_form(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
