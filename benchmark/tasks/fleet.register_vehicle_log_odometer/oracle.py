"""Oracle for fleet.register_vehicle_log_odometer.

Navigate to the Fleet app, create a new vehicle (Tesla Motors/Model 3 with
license plate BENCH-001), save it, then open the Odometers list and create
a new odometer log with value 1250 for that vehicle.
"""

from benchmark.oracle_helpers import (
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/fleet")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # --- Step 1: create the vehicle ---
    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # Model is a many2one to fleet.vehicle.model; select the existing "Model 3"
    set_many2one(page, "model_id", "Model 3")
    page.wait_for_timeout(500)

    # License plate
    fill_field(page, "license_plate", "BENCH-001")
    page.wait_for_timeout(300)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # --- Step 2: navigate to Odometers list and create a log ---
    # The Fleet app's Odometer submenu is at /odoo/action-fleet.fleet_vehicle_odometer_action
    navigate(page, "/odoo/action-fleet.fleet_vehicle_odometer_action")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # The odometer list view is editable-inline; when clicking New, Odoo
    # inserts a new row. Depending on the mode (list vs form), we may need
    # to set vehicle and value inline or via form fields. We use form-style
    # helpers which also work for list inline editing because set_many2one
    # and fill_field search by the [name=...] attribute.
    set_many2one(page, "vehicle_id", "BENCH-001")
    page.wait_for_timeout(500)

    fill_field(page, "value", "1250")
    page.wait_for_timeout(300)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
