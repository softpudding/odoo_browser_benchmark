"""Oracle for hr_recruitment.add_skill_move_stage."""

from benchmark.oracle_helpers import (
    click_kanban_card,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)

    click_kanban_card(page, "Backend Platform Engineer")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_kanban_card(page, "Jordan Park")
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    stage_btn = page.locator(
        ".o_statusbar_status button:has-text('First Interview')"
    )
    if stage_btn.count() > 0:
        stage_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    click_tab(page, "Skills")
    page.wait_for_timeout(800)

    page.get_by_role("button", name="Pick a skill from the list").click()
    page.wait_for_timeout(1000)

    modal = page.locator(".modal:visible").last
    if modal.count() > 0:
        modal.locator(
            ".o_field_widget[name='skill_type_id'] .o_selection_badge:has-text('IT Skills')"
        ).first.click()
        page.wait_for_timeout(400)
        modal.locator(
            ".o_field_widget[name='skill_id'] .o_selection_badge:has-text('Python')"
        ).first.click()
        page.wait_for_timeout(400)
        modal.locator(
            ".o_field_widget[name='skill_level_id'] .o_selection_badge:has-text('Advanced')"
        ).first.click()
        page.wait_for_timeout(400)
        modal.locator(
            ".modal-footer button.o_form_button_save, .modal-footer button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1200)
        _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
