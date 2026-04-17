"""Oracle for mail.send_direct_message_to_user.

Open Discuss, start a DM with Priya Mehta, send the required sentence.
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

    # The Discuss sidebar shows a Direct Messages category. Hover it to
    # reveal the '+' button and click it.
    dm_header = page.locator(
        ".o-mail-DiscussSidebarCategory:has-text('Direct messages')"
    ).first
    dm_header.wait_for(state="visible", timeout=15000)
    dm_header.hover()
    page.wait_for_timeout(500)
    add_dm = page.locator(
        ".o-mail-DiscussSidebarCategory:has-text('Direct messages') "
        ".o-mail-DiscussSidebarCategory-actions button"
    ).first
    add_dm.click()
    page.wait_for_timeout(800)

    # A popup/autocomplete appears asking who to DM. Type Priya.
    input_search = page.locator(
        ".o-discuss-ChannelSelector input:visible, "
        "input[placeholder*='name' i]:visible"
    )
    input_search.first.click()
    input_search.first.fill("Priya")
    page.wait_for_timeout(700)
    # Pick Priya Mehta from suggestions.
    suggestion = page.locator(
        ".o-mail-AutocompleteSelectorOption:has-text('Priya Mehta'):visible, "
        "li:has-text('Priya Mehta'):visible, "
        "a:has-text('Priya Mehta'):visible"
    )
    suggestion.first.click()
    page.wait_for_timeout(500)

    # Some Discuss versions auto-open the DM; others need a "Start" button.
    start_btn = page.locator(
        "button:has-text('Start'):visible, button:has-text('Create'):visible"
    )
    if start_btn.count() > 0:
        try:
            start_btn.first.click()
        except Exception:
            pass
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Post the message into the composer.
    composer = page.locator(
        ".o-mail-Composer-input:visible, "
        "textarea[placeholder*='Message' i]:visible"
    )
    composer.first.click()
    composer.first.fill(MESSAGE)
    page.wait_for_timeout(300)
    # Press Enter or click the Send button.
    send_btn = page.locator(
        "button[aria-label='Send message']:visible, "
        "button.o-mail-Composer-send:visible, "
        "button:has-text('Send'):visible"
    )
    if send_btn.count() > 0:
        send_btn.first.click()
    else:
        composer.first.press("Enter")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
