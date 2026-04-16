"""Oracle for project.convert_task_to_subtask."""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    click_kanban_card(page, "Atlas Support Rollout")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_kanban_card(page, "Vendor readiness checklist")
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    page.locator(".o_cp_action_menus .dropdown-toggle").first.click()
    page.wait_for_timeout(600)
    page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Convert to Task/Sub-Task')"
    ).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last
    if modal.count() > 0:
        field = modal.locator(".o_field_widget[name='parent_id'] input").first
        field.click()
        field.fill("")
        field.fill("Launch coordination")
        page.wait_for_timeout(800)
        modal.locator(".dropdown-menu .dropdown-item").get_by_text(
            "Launch coordination", exact=True
        ).first.click()
        page.wait_for_timeout(400)
        modal.locator(
            "button:has-text('Convert Task'), button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1200)
        _wait_no_loading(page)
        _wait_for_ready(page)


run_oracle(oracle)
