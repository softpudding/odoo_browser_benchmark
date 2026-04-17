"""Oracle for hr_holidays.refuse_leave_with_reason."""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


REASON_TEXT = "Denied: conflicts with critical project deadline"


def oracle(page):
    login(page)
    navigate(page, "/odoo/time-off-approval")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(400)
        except Exception:
            break
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    click_list_row(page, "Personal emergency")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    refuse_btn = page.locator(
        ".o_form_statusbar button[name='action_refuse']:visible"
    )
    if refuse_btn.count() > 0:
        refuse_btn.first.click()
    else:
        page.locator("button[name='action_refuse']:visible").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    chatter = page.locator(".o-mail-Chatter, .o_chatter")
    if chatter.count() > 0:
        chatter.first.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

    send_msg_btn = page.locator(
        "button:has-text('Send message'), "
        ".o-mail-Chatter button:has-text('Send message'), "
        ".o_Chatter button:has-text('Send message')"
    ).first
    send_msg_btn.click()
    page.wait_for_timeout(800)

    composer = page.locator(
        ".o-mail-Composer .o-mail-Composer-input, "
        ".o-mail-composer [contenteditable='true'], "
        "div[contenteditable='true'].odoo-editor-editable, "
        ".o-mail-Composer-input [contenteditable='true']"
    ).last
    composer.click()
    page.wait_for_timeout(300)
    composer.fill(REASON_TEXT)
    page.wait_for_timeout(300)

    send_btn = page.locator(
        "button.o-mail-Composer-send, "
        ".o-mail-Composer button:has-text('Send'), "
        ".o-mail-Composer button[type='submit']"
    ).first
    send_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
