"""Oracle for mail.pin_and_reply_in_chatter."""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


CHANNEL_NAME = "Morning Standups Alpha"
SEEDED_BODY = "Print queue alert from warehouse B"
REPLY_BODY = "Acknowledged - investigating now"


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Open the channel in the sidebar. The sidebar category may be collapsed;
    # try clicking the channel directly first.
    channel_btn = page.locator(
        f".o-mail-DiscussSidebarChannel:has-text('{CHANNEL_NAME}')"
    ).first
    if channel_btn.count() == 0 or not channel_btn.is_visible():
        # Expand the "Channels" category if the item is not visible
        cat_toggler = page.locator(
            ".o-mail-DiscussSidebarCategory-toggler:has-text('Channels')"
        ).first
        if cat_toggler.count() > 0:
            cat_toggler.click()
            page.wait_for_timeout(500)
        channel_btn = page.locator(
            f".o-mail-DiscussSidebarChannel:has-text('{CHANNEL_NAME}')"
        ).first
    channel_btn.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Locate the seeded message in the thread
    message = page.locator(
        f".o-mail-Message:has-text('{SEEDED_BODY}')"
    ).first
    message.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    message.hover()
    page.wait_for_timeout(500)

    # The action toolbar appears on hover. The Pin action has title="Pin".
    pin_btn = page.locator(
        ".o-mail-Message-actions button[title='Pin'], "
        ".o-mail-MessageActionList button[title='Pin']"
    ).first
    if pin_btn.count() == 0 or not pin_btn.is_visible():
        # Fallback: open the "..." menu
        message.hover()
        page.wait_for_timeout(300)
        more_btn = page.locator(
            ".o-mail-Message-actions button[title='Expand']"
        ).first
        if more_btn.count() > 0:
            more_btn.click()
            page.wait_for_timeout(300)
        pin_btn = page.locator(
            "button[title='Pin'], .o-dropdown-item:has-text('Pin')"
        ).first
    pin_btn.click()
    page.wait_for_timeout(800)

    # Confirmation dialog: "Yeah, pin it!"
    confirm_btn = page.locator(
        ".modal button:has-text('Yeah, pin it'), "
        ".o_dialog button:has-text('Yeah, pin it')"
    ).first
    if confirm_btn.count() > 0:
        confirm_btn.click()
        page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Type reply in the channel composer
    composer = page.locator(
        ".o-mail-Composer-input, "
        ".o-mail-Composer [contenteditable='true']"
    ).last
    composer.click()
    page.wait_for_timeout(300)
    composer.fill(REPLY_BODY)
    page.wait_for_timeout(300)

    send_btn = page.locator(
        "button.o-mail-Composer-send:visible, "
        ".o-mail-Composer button:has-text('Send'):visible"
    ).first
    if send_btn.count() > 0:
        send_btn.click()
    else:
        composer.press("Enter")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
