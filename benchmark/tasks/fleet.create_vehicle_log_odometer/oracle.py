"""Oracle for fleet.create_vehicle_log_odometer."""

from benchmark.oracle_helpers import (
    click_create,
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
    navigate(page, "/odoo/fleet")
    _wait_no_loading(page)

    click_create(page)
    _wait_for_ready(page)

    set_many2one(page, "model_id", "Falcon X")
    fill_field(page, "license_plate", "OPS-7421")
    set_many2one(page, "driver_id", "OdooBot")
    fill_field(page, "odometer", "12540")

    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
