"""Oracle for purchase.cancel_rfq_log_note."""

from benchmark.oracle_helpers import (
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


NOTE_TEXT = "Vendor asked us to pause this request until next quarter."


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    ensure_list_view(page)
    page.wait_for_timeout(500)
    click_list_row(page, "P-RFQ-CANCEL-01")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    page.locator(".o-mail-Chatter, .o_chatter").first.scroll_into_view_if_needed()
    page.wait_for_timeout(400)

    page.locator(
        "button.o-mail-Chatter-logNote, "
        "button:has-text('Log note'), "
        ".o-mail-Chatter button:has-text('Log note')"
    ).first.click()
    page.wait_for_timeout(700)

    note_input = page.locator(
        ".o-mail-Composer .o-mail-Composer-input, "
        ".o-mail-composer [contenteditable='true'], "
        ".o_mail_composer_input textarea, "
        "div[contenteditable='true'].odoo-editor-editable"
    ).last
    note_input.click()
    page.wait_for_timeout(200)
    try:
        note_input.fill(NOTE_TEXT)
    except Exception:
        page.keyboard.type(NOTE_TEXT)
    page.wait_for_timeout(300)

    page.locator(
        "button.o-mail-Composer-send, "
        "button:has-text('Add'), "
        ".o-mail-Composer button[type='submit']"
    ).first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    cancel_btn = page.locator(
        "button[name='button_cancel']:visible, "
        ".o_statusbar_buttons button:visible:has-text('Cancel')"
    ).first
    cancel_btn.click()
    page.wait_for_timeout(800)

    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button.btn-primary:visible, "
            "button:has-text('Ok'):visible, "
            "button:has-text('Confirm'):visible"
        ).first.click()
        page.wait_for_timeout(600)
    _wait_no_loading(page)


run_oracle(oracle)
