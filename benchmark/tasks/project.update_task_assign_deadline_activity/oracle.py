"""Oracle for project.update_task_assign_deadline_activity."""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


def _click_stage(page, stage_name):
    button = page.locator(
        f".o_statusbar_status button:has-text('{stage_name}'), "
        f".o_field_widget[name='stage_id'] .o_arrow_button:has-text('{stage_name}')"
    )
    if button.count() > 0:
        button.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    click_kanban_card(page, "Customer Portal Refresh")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    task_card = page.locator(
        ".o_kanban_record:has-text('Revise FAQ copy'), "
        ".o_card:has-text('Revise FAQ copy')"
    ).first
    task_card.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    _click_stage(page, "In Progress")

    chatter = page.locator(".o-mail-Chatter, .o_chatter")
    if chatter.count() > 0:
        chatter.first.scroll_into_view_if_needed()
        page.wait_for_timeout(400)

    page.locator(
        "button.o-mail-Chatter-activity:visible, "
        ".o-mail-Chatter button:has-text('Activities'):visible, "
        ".o-mail-Chatter button:has-text('Activity'):visible, "
        ".o_ChatterTopbar button:has-text('Activities'):visible, "
        ".o_ChatterTopbar button:has-text('Activity'):visible"
    ).first.click()
    page.wait_for_timeout(1000)

    page.wait_for_selector(
        ".modal:visible .o_field_widget[name='summary'] input",
        timeout=10000,
    )
    call_badge = page.locator(
        ".modal:visible .o_field_widget[name='activity_type_id'] .o_selection_badge:has-text('Call')"
    )
    if call_badge.count() > 0:
        call_badge.last.click()
        page.wait_for_timeout(300)

    summary = page.locator(
        ".modal:visible .o_field_widget[name='summary'] input"
    ).last
    summary.click()
    summary.fill("Review FAQ revisions")
    summary.press("Tab")
    page.wait_for_timeout(300)

    deadline = page.locator(
        ".modal:visible .o_field_widget[name='date_deadline']"
    ).last
    deadline.click()
    page.wait_for_timeout(300)
    date_input = page.locator(
        ".modal:visible .o_field_widget[name='date_deadline'] input"
    ).last
    date_input.fill("")
    date_input.type("05/20/2026")
    date_input.press("Tab")
    page.wait_for_timeout(300)

    page.locator(".modal:visible button:has-text('Save')").last.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
