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

    chatter = page.locator("#chatter, .o-mail-Chatter").first
    chatter.scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    log_note_btn = page.locator(
        "button.o-mail-Chatter-logNote, "
        "button:has-text('Log note'), "
        ".o-mail-Chatter button:has-text('Log note')"
    ).first
    log_note_btn.click()
    page.wait_for_timeout(500)
    composer = page.locator("textarea.o-mail-Composer-input:visible").first
    composer.click()
    page.wait_for_timeout(300)
    composer.type(NOTE_TEXT)
    page.wait_for_timeout(400)
    page.locator(
        "button.o-mail-Composer-send:visible, "
        ".o-mail-Composer-send:visible"
    ).first.click()
    page.wait_for_timeout(5000)
    _wait_no_loading(page)

    cancel_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Cancel'), "
        ".o_control_panel button:visible:has-text('Cancel')"
    ).first
    cancel_btn.click()
    page.wait_for_timeout(800)

    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Ok'), "
            "button:has-text('OK'), "
            "button:has-text('Confirm'), "
            "button:has-text('Cancel')"
        ).last.click()
        page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
