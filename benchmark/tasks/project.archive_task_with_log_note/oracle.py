"""Oracle for project.archive_task_with_log_note.

Open project Nexus Platform Launch, open task 'Retire beta build',
post log note with expected text, then archive via Action menu.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    click_list_row,
    ensure_list_view,
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
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Open the target task — switch to list view for reliable text search
    try:
        ensure_list_view(page)
    except Exception:
        pass
    page.wait_for_timeout(500)
    click_list_row(page, "Retire beta build")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Chatter: click Log note button and post the note
    log_note_btn = page.locator(
        "button.o-mail-Chatter-logNote, "
        "button:has-text('Log note'), "
        ".o-mail-Chatter button:has-text('Log note')"
    ).first
    log_note_btn.click()
    page.wait_for_timeout(800)

    note_input = page.locator(
        ".o-mail-Composer .o-mail-Composer-input, "
        ".o-mail-composer [contenteditable='true'], "
        ".o_mail_composer_input textarea, "
        "div[contenteditable='true'].odoo-editor-editable"
    ).last
    note_input.click()
    page.wait_for_timeout(300)
    note_input.fill(EXPECTED_NOTE)
    page.wait_for_timeout(300)

    add_btn = page.locator(
        "button:has-text('Add'), "
        "button.o-mail-Composer-send, "
        ".o-mail-Composer button[type='submit']"
    ).first
    add_btn.click()
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
