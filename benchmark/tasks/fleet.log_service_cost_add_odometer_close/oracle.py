"""Oracle for fleet.log_service_cost_add_odometer_close.

Navigate to Fleet, open the seeded BENCH-TRUCK-01 vehicle, click its
Services smart button, create a new service record with service type,
date, cost, vendor, and odometer, save, then click 'Done' on the
clickable statusbar to close the record.
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

    # Open the seeded vehicle.
    click_list_row(page, "BENCH-TRUCK-01")
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # Click the Services stat button.
    click_stat_button(page, "Services")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Click New.
    click_create(page)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Fill the service form. The form has two columns:
    #   left: description, service_type_id, date, amount, vendor_id
    #   right: vehicle_id (prefilled), purchaser_id, odometer + odometer_unit
    set_many2one(page, "service_type_id", "Oil Change")
    page.wait_for_timeout(300)
    set_date(page, "date", "04/15/2026")
    page.wait_for_timeout(300)
    fill_field(page, "amount", "120.00")
    page.wait_for_timeout(300)
    set_many2one(page, "vendor_id", "Bench Garage")
    page.wait_for_timeout(300)

    # Odometer field lives in the right column; fill_field matches by
    # [name='odometer'] attribute, which is unique inside the form.
    fill_field(page, "odometer", "25000")
    page.wait_for_timeout(300)

    save_form(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # State statusbar: the `state` field uses widget='statusbar' with
    # options={'clickable': '1'}. Click the Done button.
    done_btn = page.locator(
        ".o_statusbar_status button.o_arrow_button:has-text('Done'):visible, "
        ".o_statusbar_status button:has-text('Done'):visible"
    ).first
    done_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Re-save to persist the state change in case autosave did not fire.
    try:
        save_form(page)
    except Exception:
        pass
    _wait_no_loading(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
