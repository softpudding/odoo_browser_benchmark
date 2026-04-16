"""Oracle for hr.add_employee_skill.

Find employee Priya Mehta, open Resume tab, click 'Pick a skill from the list',
in the dialog select: Category=IT Skills, Skill=Python, Level=Advanced,
then Save & Close, then save the employee form.

In Odoo 19, the skill dialog uses o_selection_badge buttons (not dropdowns).
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

EMPLOYEE_NAME = "Priya Mehta"
SKILL_TYPE = "IT Skills"
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

    # Navigate to the Resume tab
    click_tab(page, "Resume")
    page.wait_for_timeout(1000)

    # Click "Pick a skill from the list" button
    pick_btn = page.locator('button:has-text("Pick a skill from the list")').first
    pick_btn.wait_for(state="visible", timeout=10000)
    pick_btn.click()
    page.wait_for_timeout(800)

    # The modal "Update Skills" opens with badge selection
    modal = page.locator('.modal.d-block:visible').first
    modal.wait_for(state="visible", timeout=10000)

    # Select Category: IT Skills
    skill_type_badge = modal.locator(
        f"[name='skill_type_id'] .o_selection_badge:has-text('{SKILL_TYPE}')"
    ).first
    skill_type_badge.wait_for(state="visible", timeout=5000)
    skill_type_badge.click()
    page.wait_for_timeout(500)

    # Select Skill: Python (badges refresh after category selection)
    skill_badge = modal.locator(
        f"[name='skill_id'] .o_selection_badge:has-text('{SKILL_NAME}')"
    ).first
    skill_badge.wait_for(state="visible", timeout=5000)
    skill_badge.click()
    page.wait_for_timeout(500)

    # Select Level: Advanced (badges appear after skill selection)
    level_badge = modal.locator(
        f"[name='skill_level_id'] .o_selection_badge:has-text('{SKILL_LEVEL}')"
    ).first
    level_badge.wait_for(state="visible", timeout=5000)
    level_badge.click()
    page.wait_for_timeout(300)

    # Save & Close the dialog
    save_close_btn = modal.locator('button:has-text("Save & Close")').first
    save_close_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Save the employee form
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
