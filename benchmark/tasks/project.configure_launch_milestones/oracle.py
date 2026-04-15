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
    fill_text_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_boolean,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def _open_project_kebab_action(page, project_name, action_text):
    """Open the kebab menu on a project kanban card and click an action."""
    card = page.locator(f".o_kanban_record:has-text('{project_name}')").first
    # Hover over the card to make the kebab visible
    card.hover()
    page.wait_for_timeout(300)

    # Click the kebab button inside .o_dropdown_kanban
    kebab = card.locator(".o_dropdown_kanban button, .o_dropdown_kanban .dropdown-toggle").first
    kebab.click(force=True)
    page.wait_for_timeout(500)

    # Click the action in the dropdown — use specific tag selectors to avoid
    # matching container divs. Links can be .dropdown-item or a[type="object"].
    action = page.locator(
        f"a.dropdown-item:visible:has-text('{action_text}'), "
        f"a.oe_kanban_action:visible:has-text('{action_text}'), "
        f"a[name]:visible:has-text('{action_text}')"
    ).first
    action.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # ---------------------------------------------------------------
    # Step 1: Open Atlas Redesign project form and enable Milestones
    # ---------------------------------------------------------------
    _open_project_kebab_action(page, "Atlas Redesign", "Settings")

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
    # Step 2: Create milestones via the kebab menu > Milestones
    # ---------------------------------------------------------------
    _open_project_kebab_action(page, "Atlas Redesign", "Milestones")

    def _create_milestone_inline(page, name, deadline_str):
        """Create a milestone with inline editing."""
        new_btn = page.locator(
            "button.o_list_button_add:visible, "
            ".o_control_panel button:has-text('New'):visible"
        ).first
        new_btn.click()
        page.wait_for_timeout(500)

        # The inline row should be selected; fill the name
        name_cell = page.locator(
            ".o_selected_row td[name='name'], "
            ".o_selected_row .o_field_widget[name='name']"
        ).first
        name_cell.click()
        page.wait_for_timeout(200)
        name_input = name_cell.locator("input").first
        name_input.fill(name)
        page.wait_for_timeout(300)

        # Click the deadline cell directly in the selected row
        deadline_cell = page.locator(
            ".o_selected_row td[name='deadline'], "
            ".o_selected_row .o_field_widget[name='deadline']"
        )
        if deadline_cell.count() > 0:
            deadline_cell.first.click()
            page.wait_for_timeout(500)
            # Look for input that appeared
            inp = deadline_cell.locator("input")
            if inp.count() > 0 and inp.first.is_visible():
                inp.first.click()
                inp.first.fill("")
                inp.first.type(deadline_str)
                page.wait_for_timeout(300)
            else:
                # The date cell might just need keyboard typing
                page.keyboard.type(deadline_str)
                page.wait_for_timeout(300)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

        # Save the row by clicking outside
        header = page.locator(".o_list_view thead").first
        header.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    _create_milestone_inline(page, "Prototype Freeze", "05/15/2026")
    _create_milestone_inline(page, "Launch Review", "05/29/2026")

    # ---------------------------------------------------------------
    # Step 3: Create three tasks with milestones
    # ---------------------------------------------------------------
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    click_kanban_card(page, "Atlas Redesign")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Use form view for task creation: navigate to project tasks via URL
    # and use the New button to open a form view.

    def _create_task(page, name, milestone, stage=None):
        """Create a task with given name, milestone, and optional stage."""
        # Click New in the current view
        new_btn = page.locator(
            "button.o_list_button_add:visible, "
            ".o_control_panel button:has-text('New'):visible"
        ).first
        new_btn.click()
        page.wait_for_timeout(1000)
        _wait_for_ready(page)

        # Check if we're in form view or inline edit
        form = page.locator(".o_form_view")
        if form.count() > 0:
            # Form view — task name uses widget="text" (textarea)
            fill_text_field(page, "name", name)
            page.wait_for_timeout(500)
            set_many2one(page, "milestone_id", milestone)
            page.wait_for_timeout(500)
            if stage:
                stage_btn = page.locator(f".o_statusbar_status button:has-text('{stage}')")
                if stage_btn.count() > 0:
                    stage_btn.first.click()
                    page.wait_for_timeout(500)
                    _wait_no_loading(page)
            save_form(page)
            page.wait_for_timeout(500)
            _wait_no_loading(page)
            click_breadcrumb(page, "Atlas Redesign")
            page.wait_for_timeout(500)
        else:
            # Inline list edit - type name and save
            name_input = page.locator(".o_selected_row .o_field_widget[name='name'] input, .o_selected_row input[name='display_name']")
            if name_input.count() > 0:
                name_input.first.fill(name)
                name_input.first.press("Tab")
                page.wait_for_timeout(500)
            # Save the row by clicking elsewhere or pressing Enter
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            _wait_no_loading(page)
            # Open the created task to set milestone and stage
            page.locator(f".o_data_row:has-text('{name}')").first.click()
            page.wait_for_timeout(1000)
            _wait_for_ready(page)
            set_many2one(page, "milestone_id", milestone)
            page.wait_for_timeout(500)
            if stage:
                stage_btn = page.locator(f".o_statusbar_status button:has-text('{stage}')")
                if stage_btn.count() > 0:
                    stage_btn.first.click()
                    page.wait_for_timeout(500)
                    _wait_no_loading(page)
            save_form(page)
            page.wait_for_timeout(500)
            _wait_no_loading(page)
            click_breadcrumb(page, "Atlas Redesign")
            page.wait_for_timeout(500)

    # Switch to list view
    list_btn = page.locator(
        "button.o_switch_view.o_list:visible, "
        ".o_cp_switch_buttons button.o_list:visible"
    )
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    _create_task(page, "Finalize wireframes", "Prototype Freeze", "In Progress")
    _create_task(page, "QA sign-off", "Launch Review")
    _create_task(page, "Publish landing page", "Launch Review", "Done")

    # ---------------------------------------------------------------
    # Step 4: Set project description
    # ---------------------------------------------------------------
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    _open_project_kebab_action(page, "Atlas Redesign", "Settings")

    # Click Description tab
    click_tab(page, "Description")
    page.wait_for_timeout(500)

    # Fill the description (try HTML editor first, then textarea)
    desc_editable = page.locator(
        '.o_field_widget[name="description"] .note-editable, '
        '.o_field_widget[name="description"] .odoo-editor-editable, '
        '.o_field_widget[name="description"] [contenteditable="true"], '
        '.o_field_widget[name="description"] textarea'
    )
    if desc_editable.count() > 0:
        desc_editable.first.click()
        desc_editable.first.fill("1 of 3 tasks done across 2 milestones")
    else:
        # Fallback: click the widget and type
        page.locator('.o_field_widget[name="description"]').first.click()
        page.keyboard.type("1 of 3 tasks done across 2 milestones")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)


run_oracle(oracle)
