"""Oracle for mail.mark_message_as_todo_and_resolve.

Open #benchmarks-ops, find the 3 AM warehouse sync message, click
Reply to open a thread, and post the required reply.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)

REPLY = (
    "Yes — rescheduling to 5 AM on weekdays, Ops will update the cron "
    "tonight."
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Click the #benchmarks-ops channel in the sidebar.
    channel = page.locator(
        ".o-mail-DiscussSidebarChannel:has-text('benchmarks-ops'):visible, "
        "a:has-text('benchmarks-ops'):visible"
    ).first
    channel.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Find the anchor message.
    msg = page.locator(
        ".o-mail-Message:has-text('3 AM warehouse sync'):visible"
    ).first
    msg.hover()
    page.wait_for_timeout(400)

    # Click Reply in Thread action.
    reply_btn = page.locator(
        ".o-mail-Message-actions button[title*='Reply' i]:visible, "
        ".o-mail-Message-actions button[aria-label*='Reply' i]:visible, "
        ".o-mail-Message-actions button[name='reply']:visible"
    ).first
    reply_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Type in the thread composer (appears in a side panel).
    composer = page.locator(
        ".o-mail-Thread .o-mail-Composer-input:visible, "
        ".o-mail-ChatWindow .o-mail-Composer-input:visible, "
        ".o-mail-Composer-input:visible"
    ).last
    composer.click()
    composer.fill(REPLY)
    page.wait_for_timeout(400)

    send_btn = page.locator(
        "button[aria-label='Send message']:visible, "
        "button.o-mail-Composer-send:visible"
    ).last
    if send_btn.count() > 0:
        send_btn.click()
    else:
        composer.press("Enter")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
