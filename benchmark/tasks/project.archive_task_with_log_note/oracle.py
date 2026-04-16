"""Oracle for project.archive_task_with_log_note.

Open project Nexus Platform Launch, open task 'Retire beta build',
post log note with expected text, then archive via Action menu.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


EXPECTED_NOTE = (
    "Superseded by v2 pipeline. Archiving to clear the active backlog."
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # Open the project kanban card
    click_kanban_card(page, "Nexus Platform Launch")
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # Open the target task kanban card
    click_kanban_card(page, "Retire beta build")
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # Chatter: click Log note tab and post the note
    chatter = page.locator("#chatter, .o-mail-Chatter").first
    chatter.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    page.get_by_role("tab", name="Log note").click()
    page.wait_for_timeout(500)
    composer = chatter.locator(".o-mail-Chatter-composer").first
    composer.fill(EXPECTED_NOTE)
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Log").click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Open Actions menu and click Archive
    cog = page.locator(
        ".o_cp_action_menus button:visible, "
        ".o_control_panel button.dropdown-toggle:has-text('Actions'):visible, "
        ".o_control_panel .fa-cog:visible"
    ).first
    cog.click()
    page.wait_for_timeout(500)
    archive_item = page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Archive'), "
        ".o-dropdown--menu:visible .dropdown-item:has-text('Archive')"
    ).first
    archive_item.click()
    page.wait_for_timeout(500)

    # Confirm any archival dialog that appears
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Archive'), "
            "button:has-text('OK'), "
            "button:has-text('Confirm')"
        ).first.click()
        page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
