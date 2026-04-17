"""Oracle for purchase.cancel_rfq_log_note."""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    ensure_list_view(page)
    page.wait_for_timeout(500)
    click_list_row(page, "P-RFQ-CANCEL-01")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    chatter = page.locator("#chatter, .o-mail-Chatter").first
    chatter.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    log_note = page.locator(
        "button:has-text('Log note'), .o-mail-Chatter button:has-text('Log note')"
    )
    if log_note.count() > 0:
        log_note.first.click()
    else:
        page.get_by_role("tab", name="Log note").click()
    page.wait_for_timeout(500)
    composer = chatter.locator(
        ".o-mail-Composer textarea:visible, .o-mail-Composer [contenteditable='true']:visible"
    ).first
    composer.click()
    try:
        composer.fill("Vendor asked us to pause this request until next quarter.")
    except Exception:
        page.keyboard.type("Vendor asked us to pause this request until next quarter.")
    page.wait_for_timeout(300)
    chatter.locator("button.o-mail-Composer-send:visible").first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    cancel_btn = page.locator(
        ".o_form_view .o_statusbar_buttons button:visible:has-text('Cancel'), "
        ".o_form_view button[name='button_cancel']:visible"
    ).first
    cancel_btn.click()
    page.wait_for_timeout(1200)
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Ok'), button:has-text('Confirm'), button.btn-primary"
        ).first.click()
        page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
