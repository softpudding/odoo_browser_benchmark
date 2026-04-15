"""Oracle for project.configure_launch_milestones.

Enable milestones on "Atlas Redesign" project, create two milestones via the
project card menu, create three tasks with milestone assignments, and set the
project description.
"""

from benchmark.oracle_helpers import (
    click_breadcrumb,
    click_kanban_card,
    click_create,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_boolean,
    set_date,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # ---------------------------------------------------------------
    # Step 1: Open Atlas Redesign project form and enable Milestones
    # ---------------------------------------------------------------
    # Click the ⋮ menu on the Atlas Redesign card to go to Settings
    card = page.locator(".o_kanban_record:has-text('Atlas Redesign')").first
    kebab = card.locator(".o_kanban_manage_toggle_button, button.dropdown-toggle").first
    kebab.click()
    page.wait_for_timeout(500)

    # Click Settings in the dropdown
    page.locator(".dropdown-menu a:has-text('Settings'), .o_kanban_manage_section a:has-text('Settings')").first.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)

    # Go to Settings tab and enable Milestones
    click_tab(page, "Settings")
    page.wait_for_timeout(500)

    set_boolean(page, "allow_milestones", True)
    page.wait_for_timeout(500)

    # Save and go back to project list
    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # ---------------------------------------------------------------
    # Step 2: Create milestones via the ⋮ menu > Milestones
    # ---------------------------------------------------------------
    card = page.locator(".o_kanban_record:has-text('Atlas Redesign')").first
    kebab = card.locator(".o_kanban_manage_toggle_button, button.dropdown-toggle").first
    kebab.click()
    page.wait_for_timeout(500)

    page.locator(".dropdown-menu a:has-text('Milestones'), .o_kanban_manage_section a:has-text('Milestones')").first.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)

    # Create first milestone: Prototype Freeze
    click_create(page)
    page.wait_for_timeout(500)

    fill_field(page, "name", "Prototype Freeze")
    page.wait_for_timeout(500)

    set_date(page, "deadline", "05/15/2026")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Create second milestone: Launch Review
    click_create(page)
    page.wait_for_timeout(500)

    fill_field(page, "name", "Launch Review")
    page.wait_for_timeout(500)

    set_date(page, "deadline", "05/29/2026")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # ---------------------------------------------------------------
    # Step 3: Create three tasks with milestones
    # ---------------------------------------------------------------
    # Navigate to the project's task view
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    click_kanban_card(page, "Atlas Redesign")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Switch to list view for easier task creation
    page.locator("button.o_switch_view.o_list:visible, .o_cp_switch_buttons button.o_list:visible").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # --- Task 1: "Finalize wireframes" - milestone Prototype Freeze, stage In Progress ---
    click_create(page)
    page.wait_for_timeout(500)
    _wait_for_ready(page)

    fill_field(page, "name", "Finalize wireframes")
    page.wait_for_timeout(500)

    set_many2one(page, "milestone_id", "Prototype Freeze")
    page.wait_for_timeout(500)

    # Set stage to In Progress via statusbar
    stage_btn = page.locator(".o_statusbar_status button:has-text('In Progress')").first
    stage_btn.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Go back to list
    click_breadcrumb(page, "Atlas Redesign")
    page.wait_for_timeout(500)

    # --- Task 2: "QA sign-off" - milestone Launch Review, stage New ---
    click_create(page)
    page.wait_for_timeout(500)
    _wait_for_ready(page)

    fill_field(page, "name", "QA sign-off")
    page.wait_for_timeout(500)

    set_many2one(page, "milestone_id", "Launch Review")
    page.wait_for_timeout(500)

    # New is the default stage, no need to change
    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    click_breadcrumb(page, "Atlas Redesign")
    page.wait_for_timeout(500)

    # --- Task 3: "Publish landing page" - milestone Launch Review, stage Done ---
    click_create(page)
    page.wait_for_timeout(500)
    _wait_for_ready(page)

    fill_field(page, "name", "Publish landing page")
    page.wait_for_timeout(500)

    set_many2one(page, "milestone_id", "Launch Review")
    page.wait_for_timeout(500)

    # Set stage to Done via statusbar
    stage_btn = page.locator(".o_statusbar_status button:has-text('Done')").first
    stage_btn.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # ---------------------------------------------------------------
    # Step 4: Set project description
    # ---------------------------------------------------------------
    # Navigate to project settings
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    card = page.locator(".o_kanban_record:has-text('Atlas Redesign')").first
    kebab = card.locator(".o_kanban_manage_toggle_button, button.dropdown-toggle").first
    kebab.click()
    page.wait_for_timeout(500)

    page.locator(".dropdown-menu a:has-text('Settings'), .o_kanban_manage_section a:has-text('Settings')").first.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)

    # Click Description tab
    click_tab(page, "Description")
    page.wait_for_timeout(500)

    # Fill the description (HTML editor field)
    desc_field = page.locator(".o_field_widget[name='description'] textarea, .o_field_widget[name='description'] .note-editable, .o_field_widget[name='description'] .odoo-editor-editable")
    desc_field.first.click()
    desc_field.first.fill("1 of 3 tasks done across 2 milestones")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)


run_oracle(oracle)
