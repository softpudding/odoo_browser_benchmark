"""Oracle for project.duplicate_task_assign_deadline."""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_kanban_card,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    _wait_for_ready,
    _wait_no_loading,
)


def _click_action_menu_item(page, text):
    toggle = page.locator(
        ".o_cp_action_menus .dropdown-toggle:visible, "
        ".o_control_panel button:has-text('Action'):visible, "
        ".o_control_panel button:has-text('Actions'):visible"
    )
    if toggle.count() == 0:
        raise RuntimeError("Action menu toggle not found")

    toggle.first.click()
    page.wait_for_timeout(500)

    items = page.locator(".dropdown-menu:visible .dropdown-item")
    for i in range(items.count()):
        item_text = items.nth(i).inner_text().strip()
        if text.lower() in item_text.lower():
            items.nth(i).click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)
            return

    page.press("body", "Escape")
    raise RuntimeError(f"Action menu item '{text}' not found")


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

    _click_action_menu_item(page, "Duplicate")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    fill_field(page, "name", "Draft launch checklist follow-up")
    page.wait_for_timeout(300)
    add_many2many_tag(page, "user_ids", "Mitchell Admin")
    page.wait_for_timeout(400)
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
