"""Oracle for project.complete_task_log_note.

Open project "Omega Platform Launch", find task "Write API integration spec"
in In Progress stage, move it to Done stage, then post an internal log note
with exact text via the chatter.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)

EXPECTED_NOTE = "Spec completed and reviewed by the backend team. Ready for handoff."


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # Open the project
    click_kanban_card(page, "Omega Platform Launch")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Find the target task card and click it
    task_card = page.locator(
        ".o_kanban_record:has-text('Write API integration spec'), "
        ".o_card:has-text('Write API integration spec')"
    ).first
    task_card.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Move task to Done stage using the stage bar at top of task form
    # In Odoo 19, task form has a statusbar or kanban_state widget
    done_btn = page.locator(
        ".o_statusbar_status button:has-text('Done'):visible, "
        ".o_field_widget[name='stage_id'] .o_arrow_button:has-text('Done'):visible"
    ).first
    if done_btn.count() > 0:
        done_btn.click()
    else:
        # Try the stage dropdown/select
        stage_widget = page.locator(".o_field_widget[name='stage_id']").first
        stage_widget.click()
        page.wait_for_timeout(300)
        page.locator(".o_statusbar_status button:has-text('Done'), "
                     "li:has-text('Done'), .dropdown-item:has-text('Done')").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Handle any dialog (e.g., confirm moving to Done)
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button.btn-primary").first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    # Post an internal log note in the chatter
    # Click "Log note" (not "Send message")
    log_note_btn = page.locator(
        "button.o-mail-Chatter-logNote, "
        "button:has-text('Log note'), "
        ".o-mail-Chatter button:has-text('Log note'), "
        "a:has-text('Log note')"
    ).first
    log_note_btn.click()
    page.wait_for_timeout(800)

    # Type the note text into the composer
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

    # Click Add to post the note
    add_btn = page.locator(
        "button:has-text('Add'), "
        "button.o-mail-Composer-send, "
        ".o-mail-Composer button[type='submit']"
    ).first
    add_btn.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
