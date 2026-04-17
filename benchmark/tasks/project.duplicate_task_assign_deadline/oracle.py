"""Oracle for project.duplicate_task_assign_deadline."""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    _wait_no_loading,
    _wait_for_ready,
)


def _fill_task_name(page, value: str) -> None:
    widget = page.locator(".o_field_widget[name='name']").first
    widget.click()
    page.wait_for_timeout(300)
    editor = widget.locator("input:visible, textarea:visible, [contenteditable='true']:visible").first
    editor.click()
    tag_name = editor.evaluate("el => el.tagName.toLowerCase()")
    if tag_name in {"input", "textarea"}:
        editor.fill("")
        editor.fill(value)
        editor.press("Tab")
    else:
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(value)
        editor.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    click_kanban_card(page, "Launch Enablement Board")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_kanban_card(page, "Prepare webinar outline")
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    actions = page.locator(
        ".o_cp_action_menus button:visible, "
        ".o_control_panel button.dropdown-toggle:has-text('Actions'):visible, "
        ".o_control_panel .fa-cog:visible"
    ).first
    actions.click()
    page.wait_for_timeout(500)
    page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Duplicate'), "
        ".o-dropdown--menu:visible .dropdown-item:has-text('Duplicate')"
    ).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    _fill_task_name(page, "Prepare webinar outline - APAC")
    page.wait_for_timeout(400)
    set_date(page, "date_deadline", "06/24/2026")
    page.wait_for_timeout(400)

    stage_btn = page.locator(
        ".o_statusbar_status button:has-text('In Progress'), "
        ".o_field_widget[name='stage_id'] button:has-text('In Progress')"
    )
    if stage_btn.count() > 0:
        stage_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
