"""Oracle for fleet.schedule_vehicle_service_activity.

Navigate to Fleet, open the seeded vehicle, and schedule a To-Do
activity via the chatter with the required summary and due date.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    schedule_activity,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/fleet")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Open the seeded vehicle
    click_list_row(page, "Benchmark Utility Truck")
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # Schedule the activity via the chatter
    schedule_activity(
        page,
        activity_type="To-Do",
        summary="Yearly Safety Inspection",
        due_date="07/20/2026",
    )
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
