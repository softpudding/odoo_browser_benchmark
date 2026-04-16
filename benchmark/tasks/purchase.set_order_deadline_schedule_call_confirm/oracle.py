"""Oracle for purchase.set_order_deadline_schedule_call_confirm."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    schedule_activity,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "MED-RFQ-ACT-01")
    page.wait_for_timeout(800)

    fill_field(page, "partner_ref", "BPI-DOCK-05")
    page.wait_for_timeout(400)
    save_form(page)
    page.wait_for_timeout(400)

    schedule_activity(
        page,
        activity_type="Call",
        summary="Confirm dock appointment",
        due_date="05/18/2026",
    )
    page.wait_for_timeout(400)

    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
