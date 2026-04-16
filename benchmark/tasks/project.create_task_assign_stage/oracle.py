"""Oracle for project.create_task_assign_stage.

Open "Omega Platform Launch" project, create a new task "Design Landing
Page Mockup" in "In Progress" stage with assignee, deadline, priority,
and description.
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_breadcrumb,
    click_kanban_card,
    ensure_list_view,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    _wait_no_loading,
    _wait_for_ready,
)


TASK_NAME = "Design Landing Page Mockup"


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # Open the project
    click_kanban_card(page, "Omega Platform Launch")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Switch to list view so "New" either opens a form or an inline row
    ensure_list_view(page)
    page.wait_for_timeout(500)

    # Click New
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    form = page.locator(".o_form_view").first

    # Task name — textarea widget in form view, input in inline list
    if form.count() > 0 and form.is_visible():
        fill_text_field(page, "name", TASK_NAME)
    else:
        name_input = page.locator(
            ".o_selected_row .o_field_widget[name='name'] input, "
            ".o_selected_row .o_field_widget[name='name'] textarea, "
            ".o_selected_row input[name='display_name']"
        ).first
        name_input.fill(TASK_NAME)
        page.wait_for_timeout(400)
        # Save the inline row then open it
        page.keyboard.press("Enter")
        page.wait_for_timeout(800)
        _wait_no_loading(page)
        page.locator(f".o_data_row:has-text('{TASK_NAME}')").first.click()
        page.wait_for_timeout(1000)
        _wait_for_ready(page)

    # Set assignee (user_ids is a many2many).
    # Inline picker — avoid the "Create 'Administrator'" quick-create option.
    user_input = page.locator(
        ".o_field_widget[name='user_ids'] input"
    ).first
    user_input.click()
    user_input.fill("Administrator")
    page.wait_for_timeout(800)
    # Pick the existing user (first dropdown-item without "Create")
    items = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item"
    )
    picked = False
    for i in range(items.count()):
        txt = items.nth(i).inner_text().strip()
        if "Create" in txt or "create" in txt:
            continue
        if "Administrator" in txt:
            items.nth(i).click()
            picked = True
            break
    if not picked:
        items.first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Set deadline
    set_date(page, "date_deadline", "05/15/2026")
    page.wait_for_timeout(500)

    # Set priority to Urgent (1 star)
    priority_widget = page.locator(".o_field_widget[name='priority']").first
    stars = priority_widget.locator(".o_priority_star, .fa-star, .fa-star-o")
    if stars.count() > 0:
        stars.first.click()
        page.wait_for_timeout(300)

    # Set description — Odoo 19 HTML editor
    desc_field = page.locator(
        ".o_field_widget[name='description'] .note-editable, "
        ".o_field_widget[name='description'] .odoo-editor-editable, "
        ".o_field_widget[name='description'] [contenteditable='true']"
    )
    if desc_field.count() > 0:
        desc_field.first.click()
        page.keyboard.type(
            "Create wireframes for the new landing page including hero section and feature grid."
        )
        page.wait_for_timeout(500)

    # Set stage to "In Progress" via the status bar
    stage_btn = page.locator(
        ".o_statusbar_status button:has-text('In Progress')"
    )
    if stage_btn.count() > 0:
        stage_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    # Save the form
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
