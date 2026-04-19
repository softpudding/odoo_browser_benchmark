"""Oracle for project_todo.create_note_set_color_deadline."""

from benchmark.oracle_helpers import (
    _wait_no_loading,
    login,
    navigate,
    run_oracle,
)


TARGET_NAME = "Crane Audit Memo"


def _ensure_kanban_view(page) -> None:
    kanban_btn = page.locator(
        "button.o_switch_view.o_kanban:visible, "
        ".o_cp_switch_buttons button.o_kanban:visible"
    )
    if kanban_btn.count() > 0:
        kanban_btn.first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)


def _set_non_default_card_color(page) -> None:
    card = page.locator(f".o_kanban_view .o_kanban_record:has-text('{TARGET_NAME}')").first
    card.wait_for(state="visible", timeout=15000)
    card.hover()
    page.wait_for_timeout(400)

    kebab = card.locator(
        ".o_dropdown_kanban button, .o_dropdown_kanban .dropdown-toggle"
    ).first
    kebab.click(force=True)
    page.wait_for_timeout(500)

    color_option = page.locator(
        ".o-dropdown--kanban-record-menu:visible .o_kanban_colorpicker "
        "button:not(.active):visible"
    ).first
    color_option.wait_for(state="visible", timeout=10000)
    color_option.click(force=True)
    page.wait_for_timeout(700)
    _wait_no_loading(page)


def _create_note(page) -> None:
    page.get_by_text("New", exact=True).click()
    page.wait_for_timeout(800)

    quick_create = page.locator(".o_kanban_quick_create:visible").first
    quick_create.wait_for(state="visible", timeout=10000)

    quick_create.locator("[name='display_name'] input").first.fill(TARGET_NAME)
    deadline_input = quick_create.locator("[name='date_deadline'] input").first
    deadline_input.click()
    deadline_input.fill("")
    deadline_input.type("05/20/2026")
    deadline_input.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    quick_create.locator(".o_kanban_add").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/to-do")
    _create_note(page)

    navigate(page, "/odoo/to-do")
    _ensure_kanban_view(page)
    _set_non_default_card_color(page)


run_oracle(oracle)
