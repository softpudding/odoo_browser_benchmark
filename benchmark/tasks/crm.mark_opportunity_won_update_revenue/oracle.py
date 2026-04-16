"""Oracle for crm.mark_opportunity_won_update_revenue.

Open the target opportunity among distractors, set expected_revenue to 52000,
then click the status-bar Won button.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


TARGET = "Crestline Networks - Managed VPN"


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Open the target opportunity kanban card
    click_kanban_card(page, TARGET)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Update expected_revenue. The field widget name is 'expected_revenue'.
    try:
        fill_field(page, "expected_revenue", "52000")
    except Exception:
        # Fallback: direct locator
        inp = page.locator(
            ".o_field_widget[name='expected_revenue'] input"
        ).first
        inp.click()
        inp.fill("")
        inp.type("52000")
        inp.press("Tab")
        page.wait_for_timeout(500)

    # Save the revenue change first so the Won action uses the latest value
    try:
        save_form(page)
    except Exception:
        pass
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Click the Won button in the status bar
    won_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Won'), "
        "button[name='action_set_won_rainbowman']:visible, "
        "button[name='action_set_won']:visible"
    ).first
    won_btn.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # If a rainbow-man effect shows, wait a bit; no dialog to dismiss
    page.wait_for_timeout(500)


run_oracle(oracle)
