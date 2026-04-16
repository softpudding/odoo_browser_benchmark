"""Oracle for crm.edit_opportunity_schedule_call.

Find opportunity "Beacon Analytics Deal", update revenue and probability,
then schedule a Call activity with date and summary.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    fill_field,
    login,
    modal_fill_field,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
)


def _schedule_call(page, summary: str, due_date: str):
    """Schedule a Call activity via chatter → wizard."""
    activity_btn = page.locator(
        "button.o-mail-Chatter-activity:visible, "
        "button:has-text('Activity'):visible"
    ).first
    activity_btn.click()
    page.wait_for_timeout(1500)
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(500)

    modal = page.locator(".modal:visible").last

    # Activity type — selection badges in Odoo 19
    badge = modal.locator(
        ".o_field_widget[name='activity_type_id'] "
        ".o_selection_badge:has-text('Call')"
    ).first
    badge.click()
    page.wait_for_timeout(500)

    # Summary
    modal_fill_field(page, "summary", summary)
    page.wait_for_timeout(300)

    # Date deadline — daterange button/input. Click to activate.
    deadline = modal.locator(".o_field_widget[name='date_deadline']").first
    # Try button first, then input fallback
    btn = deadline.locator("button").first
    if btn.count() > 0 and btn.is_visible():
        btn.click()
    else:
        inp_pre = deadline.locator("input").first
        inp_pre.click()
    page.wait_for_timeout(700)

    # After activation the input should be present and visible
    inp = deadline.locator("input").first
    inp.click(click_count=3)
    inp.fill("")
    inp.type(due_date)
    inp.press("Tab")
    page.wait_for_timeout(500)

    # Defocus datepicker by clicking modal header (avoid Escape which closes modal)
    modal.locator(".modal-header").first.click()
    page.wait_for_timeout(300)

    # Save
    save_btn = modal.locator(
        ".modal-footer button:has-text('Schedule'), "
        ".modal-footer button:has-text('Save')"
    ).first
    save_btn.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


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
    _schedule_call(page, "Follow up on proposal", "05/10/2026")


run_oracle(oracle)
