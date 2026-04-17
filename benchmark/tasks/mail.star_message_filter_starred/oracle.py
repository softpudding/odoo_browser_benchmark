"""Oracle for mail.star_message_filter_starred.

Open Discuss Inbox, hover the Finance close blocker message, click star.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Click Inbox sidebar entry (usually the default view).
    inbox = page.locator(
        "button:has-text('Inbox'):visible, a:has-text('Inbox'):visible, "
        ".o-mail-DiscussSidebar-item:has-text('Inbox'):visible"
    )
    if inbox.count() > 0:
        inbox.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Find the target message by its subject text.
    msg = page.locator(
        ".o-mail-Message:has-text('Finance close blocker'):visible"
    ).first
    msg.hover()
    page.wait_for_timeout(400)

    # Click the star action in the message hover toolbar.
    star_btn = page.locator(
        ".o-mail-Message-actions button[title*='star' i]:visible, "
        ".o-mail-Message-actions button[title*='Bookmark' i]:visible, "
        ".o-mail-Message-actions button[aria-label*='Mark as Todo' i]:visible, "
        ".o-mail-Message-actions button[title*='Mark as Todo' i]:visible"
    ).first
    star_btn.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
