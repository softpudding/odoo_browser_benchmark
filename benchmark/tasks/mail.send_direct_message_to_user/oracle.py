"""Oracle for mail.send_direct_message_to_user.

Open Discuss, click the pre-seeded DM thread with Priya Mehta, send
the required sentence.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)

MESSAGE = (
    "The 10:00 product sync is moved to Thursday 14:00 — please update "
    "your calendar."
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # The seed pre-created a DM with Priya. Click it in the sidebar.
    dm_item = page.locator(
        ".o-mail-DiscussSidebar a:has-text('Priya Mehta'), "
        ".o-mail-DiscussSidebarChannel:has-text('Priya Mehta')"
    ).first
    dm_item.wait_for(state="visible", timeout=15000)
    dm_item.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Focus the composer and type the message. The composer is a
    # textarea with class o-mail-Composer-input.
    composer = page.locator("textarea.o-mail-Composer-input:visible").last
    composer.wait_for(state="visible", timeout=10000)
    composer.click()
    composer.fill(MESSAGE)
    page.wait_for_timeout(500)

    # Send by clicking the send button, or Ctrl/Cmd+Enter as fallback.
    send_btn = page.locator(
        "button[aria-label='Send message']:visible, "
        "button.o-mail-Composer-send:visible, "
        "button[title='Send' i]:visible"
    )
    if send_btn.count() > 0:
        try:
            send_btn.first.click(timeout=3000)
        except Exception:
            composer.press("Enter")
    else:
        composer.press("Enter")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
