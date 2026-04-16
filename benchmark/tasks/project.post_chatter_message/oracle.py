"""Oracle for project.post_chatter_message.

Open project "Omega Platform Launch", find task "Write API integration spec",
and post a regular message in the chatter with exact text.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_kanban_card,
)

EXPECTED_MESSAGE = "Backend team has reviewed the spec. Moving forward with implementation."


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Open the project "Omega Platform Launch"
    click_kanban_card(page, "Omega Platform Launch")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Find and click the target task card
    task_card = page.locator(
        ".o_kanban_record:has-text('Write API integration spec'), "
        ".o_card:has-text('Write API integration spec')"
    ).first
    task_card.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Scroll down to make the chatter visible
    chatter = page.locator(".o-mail-Chatter, .o_chatter")
    if chatter.count() > 0:
        chatter.first.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

    # Click "Send message" to activate the chatter composer
    send_msg_btn = page.locator(
        "button:has-text('Send message'), "
        ".o-mail-Chatter button:has-text('Send message'), "
        ".o_Chatter button:has-text('Send message')"
    ).first
    send_msg_btn.click()
    page.wait_for_timeout(800)

    # Type the message into the composer
    # In Odoo 19, the composer uses a contenteditable div or textarea
    composer = page.locator(
        ".o-mail-Composer .o-mail-Composer-input, "
        ".o-mail-composer [contenteditable='true'], "
        ".o_mail_composer_input textarea, "
        "div[contenteditable='true'].odoo-editor-editable, "
        ".o-mail-Composer-input [contenteditable='true']"
    ).last
    composer.click()
    page.wait_for_timeout(300)
    composer.fill(EXPECTED_MESSAGE)
    page.wait_for_timeout(300)

    # Click Send to post the message
    send_btn = page.locator(
        "button.o-mail-Composer-send, "
        ".o-mail-Composer button:has-text('Send'), "
        ".o-mail-Composer button[type='submit']"
    ).first
    send_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
