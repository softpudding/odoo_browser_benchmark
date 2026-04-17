"""Oracle for fleet.create_vehicle_log_odometer.

Create a vehicle (Audi A4, plate BENCH-FL-01), then log an odometer
reading of 15200 dated June 1, 2026.
"""

from benchmark.oracle_helpers import (
    click_create,
    click_stat_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/fleet")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Create a new vehicle
    click_create(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Set model (Audi A4)
    set_many2one(page, "model_id", "A4")
    page.wait_for_timeout(500)

    # Set license plate
    fill_field(page, "license_plate", "BENCH-FL-01")
    page.wait_for_timeout(300)

    # Set driver to Mitchell Admin
    set_many2one(page, "driver_id", "Mitchell Admin")
    page.wait_for_timeout(500)

    # Save the vehicle
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Navigate to odometer via the Odometer smart button or direct field
    # Try clicking the odometer stat button
    try:
        click_stat_button(page, "Odometer")
    except Exception:
        # Try the odometer field link
        odom_link = page.locator(
            ".oe_stat_button:has-text('Odometer'):visible, "
            "a:has-text('Odometer'):visible, "
            ".o_field_widget[name='odometer']:visible"
        ).first
        odom_link.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Create new odometer entry
    click_create(page)
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Set odometer value
    fill_field(page, "value", "15200")
    page.wait_for_timeout(300)

    # Set date
    set_date(page, "date", "06/01/2026")
    page.wait_for_timeout(300)

    # Save
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
