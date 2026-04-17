"""Oracle for project.duplicate_task_assign_deadline."""

from benchmark.oracle_helpers import (
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

    click_kanban_card(page, "Launch Enablement Board")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_kanban_card(page, "Prepare webinar outline")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    page.locator(".o_cp_action_menus .dropdown-toggle").first.click()
    page.wait_for_timeout(500)
    page.locator(".dropdown-menu:visible .dropdown-item").filter(
        has_text="Duplicate"
    ).first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)
    _wait_for_ready(page)

    edit_btn = page.locator(
        ".o_control_panel button:has-text('Edit'):visible, button.o_form_button_edit:visible"
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
    try:
        name_input.fill("Prepare webinar outline - APAC")
    except Exception:
        name_input.press("Control+A")
        page.keyboard.type("Prepare webinar outline - APAC")
    page.wait_for_timeout(300)
    set_date(page, "date_deadline", "06/24/2026")
    page.wait_for_timeout(300)

    progress_btn = page.locator(
        ".o_statusbar_status button:has-text('In Progress'), "
        ".o_field_widget[name='stage_id'] button:has-text('In Progress')"
    )
    if progress_btn.count() > 0:
        progress_btn.first.click()
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
