"""Oracle for project.rename_task_assign_tags_priority."""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    click_kanban_card(page, "Operations Knowledge Base")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_kanban_card(page, "Draft launch checklist")
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    edit_btn = page.locator(
        ".o_control_panel button:has-text('Edit'):visible, "
        "button.o_form_button_edit:visible"
    )
    if edit_btn.count() > 0:
        edit_btn.first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)

    name_widget = page.locator(".o_field_widget[name='name']").first
    name_widget.click()
    page.wait_for_timeout(300)
    name_input = name_widget.locator(
        "input:visible, textarea:visible, [contenteditable='true']:visible"
    ).first
    name_input.click()
    name_input.fill("Draft launch checklist follow-up")
    name_input.press("Tab")
    page.wait_for_timeout(300)
    set_date(page, "date_deadline", "05/27/2026")
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
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
