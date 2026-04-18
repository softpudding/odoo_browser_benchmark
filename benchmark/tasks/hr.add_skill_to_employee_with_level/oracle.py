"""Oracle for hr.add_skill_to_employee_with_level.

Open Tech Tom, navigate to Skills tab (in the Resume group), click
'Pick a skill from the list'. In the dialog, cascade select:
Skill Type='Programming Languages' -> Skill='Python' -> Level='Advanced'.
Save & Close the dialog, then save the employee form.

In Odoo 19 the skill dialog uses o_selection_badge buttons.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    click_tab,
    save_form,
)

EMPLOYEE_NAME = "Tech Tom"
SKILL_TYPE = "Programming Languages"
SKILL_NAME = "Python"
SKILL_LEVEL = "Advanced"


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Open the employee form
    click_list_row(page, EMPLOYEE_NAME)
    _wait_for_ready(page)

    # Navigate to the Resume tab (where Skills section lives)
    click_tab(page, "Resume")
    page.wait_for_timeout(1000)

    # Click "Pick a skill from the list" button
    pick_btn = page.locator('button:has-text("Pick a skill from the list")').first
    pick_btn.wait_for(state="visible", timeout=10000)
    pick_btn.click()
    page.wait_for_timeout(800)

    # Update Skills modal opens with badge selection
    modal = page.locator('.modal.d-block:visible').first
    modal.wait_for(state="visible", timeout=10000)

    # Select Skill Type: Programming Languages
    skill_type_badge = modal.locator(
        f"[name='skill_type_id'] .o_selection_badge:has-text('{SKILL_TYPE}')"
    ).first
    skill_type_badge.wait_for(state="visible", timeout=5000)
    skill_type_badge.click()
    page.wait_for_timeout(500)

    # Select Skill: Python (badges refresh after type selection)
    skill_badge = modal.locator(
        f"[name='skill_id'] .o_selection_badge:has-text('{SKILL_NAME}')"
    ).first
    skill_badge.wait_for(state="visible", timeout=5000)
    skill_badge.click()
    page.wait_for_timeout(500)

    # Select Level: Advanced
    level_badge = modal.locator(
        f"[name='skill_level_id'] .o_selection_badge:has-text('{SKILL_LEVEL}')"
    ).first
    level_badge.wait_for(state="visible", timeout=5000)
    level_badge.click()
    page.wait_for_timeout(300)

    # Save & Close dialog
    save_close_btn = modal.locator('button:has-text("Save & Close")').first
    save_close_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Save the employee form
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
