"""Oracle for fleet.log_service_cost_record.

Navigate to Fleet, open the seeded vehicle, click its Services stat
button, create a new service record with service type, vendor, amount,
and date, then save.
"""

from benchmark.oracle_helpers import (
    click_create,
    click_list_row,
    click_stat_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/fleet")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Open the seeded vehicle
    click_list_row(page, "Benchmark Fleet Sedan")
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # Click the Services stat button
    click_stat_button(page, "Services")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Click New
    click_create(page)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Fill fields
    set_many2one(page, "service_type_id", "Oil Change")
    set_date(page, "date", "05/10/2026")
    fill_field(page, "amount", "150.00")
    set_many2one(page, "vendor_id", "Beacon Auto Shop")

    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
