"""Oracle for fleet.schedule_vehicle_service_activity.

Open vehicle SVC-8812, schedule a 'To Do' activity with summary and
deadline via the schedule activity button in the chatter.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    schedule_activity,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/fleet")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Clear filters.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break
    _wait_no_loading(page)

    # Switch to list view for reliable click.
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)

    click_list_row(page, "SVC-8812")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    schedule_activity(
        page,
        activity_type="To-Do",
        summary="Annual inspection and service",
        due_date="06/30/2026",
    )


run_oracle(oracle)
