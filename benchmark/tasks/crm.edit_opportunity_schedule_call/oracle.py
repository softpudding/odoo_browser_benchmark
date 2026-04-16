"""Oracle for crm.edit_opportunity_schedule_call.

Find opportunity "Beacon Analytics Deal", update revenue and probability,
then schedule a Call activity with date and summary.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
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
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    # Click the opportunity card in kanban view
    click_kanban_card(page, "Beacon Analytics Deal")
    page.wait_for_timeout(500)

    # Update expected revenue
    fill_field(page, "expected_revenue", "75000")
    page.wait_for_timeout(500)

    # Update probability
    fill_field(page, "probability", "60")
    page.wait_for_timeout(500)

    # Save before scheduling activity
    save_form(page)
    page.wait_for_timeout(500)

    # Schedule Call activity
    schedule_activity(
        page,
        activity_type="Call",
        summary="Follow up on proposal",
        due_date="05/10/2026",
    )
    page.wait_for_timeout(500)


run_oracle(oracle)
