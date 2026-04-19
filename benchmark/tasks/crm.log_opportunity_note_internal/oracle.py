"""Oracle for crm.log_opportunity_note_internal.

Opens the CRM pipeline, clicks the 'Bench Note Opp' kanban card, then
uses the chatter Log-note tab to post the text 'Customer asked for demo'.
Produces a mail.message on the crm.lead with message_type='comment' and
subtype_id=mail.mt_note.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


EXPECTED_NOTE = "Customer asked for demo"


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    # Open the opportunity card in the kanban pipeline.
    click_kanban_card(page, "Bench Note Opp")
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # Scroll the chatter into view so the composer is reachable.
    chatter = page.locator("#chatter, .o-mail-Chatter").first
    chatter.scroll_into_view_if_needed()
    page.wait_for_timeout(400)

    # Click the Log note tab explicitly — even though chatter defaults
    # to Log note, making the click deterministic keeps the subtype pinned
    # to mail.mt_note.
    log_note_btn = page.locator(
        "button.o-mail-Chatter-logNote, "
        "button:has-text('Log note'), "
        ".o-mail-Chatter button:has-text('Log note'), "
        "a:has-text('Log note')"
    ).first
    log_note_btn.click()
    page.wait_for_timeout(600)

    # Type the note into whichever composer variant is visible.
    composer_input = page.locator(
        "textarea.o-mail-Composer-input:visible, "
        ".o-mail-Composer-input:visible, "
        ".o-mail-Composer [contenteditable='true']:visible, "
        "div[contenteditable='true'].odoo-editor-editable:visible"
    ).last
    composer_input.click()
    page.wait_for_timeout(200)
    try:
        composer_input.fill(EXPECTED_NOTE)
    except Exception:
        composer_input.evaluate(
            "(el, text) => { el.textContent = text;"
            " el.dispatchEvent(new Event('input', { bubbles: true })); }",
            EXPECTED_NOTE,
        )
    page.wait_for_timeout(500)

    # Click the Log button to post the internal note.
    log_btn = page.locator(
        "button.o-mail-Composer-send:has-text('Log'):visible, "
        "button.o-mail-Composer-send:visible, "
        ".o-mail-Composer-send:visible"
    ).first
    log_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
