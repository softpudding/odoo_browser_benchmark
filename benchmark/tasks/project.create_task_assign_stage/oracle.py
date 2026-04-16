"""Oracle for project.create_task_assign_stage.

Open "Omega Platform Launch" project, create a new task "Design Landing
Page Mockup" in "In Progress" stage with assignee, deadline, priority,
and description.
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_kanban_card,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # Open the project
    click_kanban_card(page, "Omega Platform Launch")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # We're now in the project's task kanban view.
    # Find the "In Progress" column and click the "+" button to create
    # a new task in that column, or click "New" and set the stage.

    # Look for the "In Progress" column and its quick-add button
    in_progress_col = page.locator(
        ".o_kanban_group:has(.o_column_title:has-text('In Progress'))"
    )

    if in_progress_col.count() > 0:
        # Click the "+" quick create in the In Progress column
        add_btn = in_progress_col.first.locator(
            ".o_kanban_quick_add, button.o_quick_add, "
            ".o_kanban_header button:visible"
        )
        if add_btn.count() > 0:
            add_btn.first.click()
            page.wait_for_timeout(500)
            # Quick create: type title and open the form
            quick_input = page.locator(
                ".o_kanban_quick_create input[type='text']:visible"
            )
            if quick_input.count() > 0:
                quick_input.first.fill("Design Landing Page Mockup")
                # Click "Add" then "Edit"
                add_btn2 = page.locator(
                    ".o_kanban_quick_create button:has-text('Add'):visible"
                )
                if add_btn2.count() > 0:
                    add_btn2.first.click()
                    page.wait_for_timeout(500)
                    _wait_no_loading(page)
                    # Now open the created card
                    click_kanban_card(page, "Design Landing Page Mockup")
                    page.wait_for_timeout(500)
            else:
                # Column add button opened form directly
                pass
        else:
            # No quick-add, use the "New" button and set stage later
            page.locator(
                "button.o_list_button_add:visible, "
                ".o_control_panel button:has-text('New'):visible"
            ).first.click()
            page.wait_for_timeout(500)
            _wait_no_loading(page)
            fill_field(page, "name", "Design Landing Page Mockup")
    else:
        # Fallback: use the New button
        page.locator(
            "button.o_list_button_add:visible, "
            ".o_control_panel button:has-text('New'):visible"
        ).first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)
        fill_field(page, "name", "Design Landing Page Mockup")

    # Now we should be on the task form
    # Set title if not already set
    name_input = page.locator(".o_field_widget[name='name'] input")
    if name_input.count() > 0:
        current = name_input.first.input_value()
        if not current or "Design Landing" not in current:
            fill_field(page, "name", "Design Landing Page Mockup")

    # Set assignee (user_ids is a many2many)
    add_many2many_tag(page, "user_ids", "Mitchell Admin")
    page.wait_for_timeout(500)

    # Set deadline
    set_date(page, "date_deadline", "05/15/2026")
    page.wait_for_timeout(500)

    # Set priority to Urgent (1 star) — click the first star
    priority_widget = page.locator(".o_field_widget[name='priority']").first
    stars = priority_widget.locator(".o_priority_star, .fa-star, .fa-star-o")
    if stars.count() > 0:
        stars.first.click()
        page.wait_for_timeout(300)

    # Set description
    desc_field = page.locator(
        ".o_field_widget[name='description'] .note-editable, "
        ".o_field_widget[name='description'] textarea, "
        ".o_field_widget[name='description'] .odoo-editor-editable"
    )
    if desc_field.count() > 0:
        desc_field.first.click()
        desc_field.first.fill(
            "Create wireframes for the new landing page including hero section and feature grid."
        )
    page.wait_for_timeout(500)

    # Set stage to "In Progress" if not already there
    # Check the status bar for stage buttons
    stage_btn = page.locator(
        ".o_statusbar_status button:has-text('In Progress')"
    )
    if stage_btn.count() > 0:
        stage_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    # Save
    save_form(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
