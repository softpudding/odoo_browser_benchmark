"""Oracle for sale.cancel_quotation_log_reason.

Open draft quotation BENCH-CANCEL-01, post log note with the reason,
then click Cancel. Confirm any dialog.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


EXPECTED_NOTE = (
    "Customer withdrew RFP. Cancelling to remove from active pipeline."
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, "BENCH-CANCEL-01")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Post log note via chatter
    page.locator(".o-mail-Chatter, .o_chatter").first.scroll_into_view_if_needed()
    page.wait_for_timeout(500)

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
        "button.o-mail-Composer-send, "
        "button:has-text('Add'), "
        ".o-mail-Composer button[type='submit']"
    ).first
    add_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Click the Cancel header button on the SO form (name=action_cancel)
    cancel_btn = page.locator(
        ".o_form_view .o_form_statusbar button[data-hotkey='x']:visible, "
        ".o_form_view header button[name='action_cancel']:visible, "
        ".o_form_view .o_statusbar_buttons button:visible:has-text('Cancel')"
    ).first
    cancel_btn.click()
    page.wait_for_timeout(800)

    # Confirmation dialog — click the primary OK/Confirm button
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button.btn-primary:visible, "
            "button:has-text('Ok'):visible, "
            "button:has-text('OK'):visible, "
            "button:has-text('Confirm'):visible"
        ).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
