"""Oracle for im_livechat.configure_channel_then_handle_widget_chat.

Single-tab variant: the seed pre-builds the live chat session with the
visitor's waiting message so the agent (and this oracle) only needs to reply
via the Discuss composer using the ::hello canned-response shortcut.

The composer is a plain textarea in Discuss (NOT the Wysiwyg editor, which is
only enabled for mail composers with HTML). The suggestion popover appears as
a `.o-mail-NavigableList-item` overlay. Typing ``::hello`` triggers the popover
(delimiter handler in `searchSuggestions`); selecting the item substitutes the
shortcut with the full text.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


SESSION_NAME = "Visitor #BENCH-359"
EXPECTED_REPLY = "Hi, thanks for reaching out!"


def _open_livechat_session(page):
    """Click the live chat session in the Discuss sidebar."""
    # Wait for the sidebar to render & fetch channels (async mail/data call).
    page.locator(".o-mail-DiscussSidebar").first.wait_for(
        state="visible", timeout=20000
    )
    # Explicitly wait until the Live Chat (im_livechat.channel) category and
    # the session both appear — initial fetch is async.
    page.wait_for_timeout(1500)

    # If the Bench Support category is collapsed, click the toggler.
    bench_cat_toggler = page.locator(
        ".o-mail-DiscussSidebarCategory-livechat .o-mail-DiscussSidebarCategory-toggler"
    )
    if bench_cat_toggler.count() > 0:
        # Expand if chevron-right (closed).
        closed_icon = bench_cat_toggler.locator(".oi-chevron-right")
        if closed_icon.count() > 0:
            bench_cat_toggler.first.click()
            page.wait_for_timeout(500)

    sidebar_item = page.locator(
        ".o-mail-DiscussSidebarChannel-itemName",
        has_text=SESSION_NAME,
    ).first
    sidebar_item.wait_for(state="visible", timeout=20000)
    sidebar_item.scroll_into_view_if_needed()
    sidebar_item.click()
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Confirm the thread header / composer is visible for this channel.
    page.locator(".o-mail-Composer-input, .o-mail-Composer").first.wait_for(
        state="visible", timeout=15000
    )


def _fire_canned_response(page):
    """Type `::hello` into the Discuss composer, pick the suggestion, send."""
    textarea = page.locator(".o-mail-Composer-input").first
    textarea.wait_for(state="visible", timeout=10000)
    textarea.click()
    textarea.focus()
    page.wait_for_timeout(300)

    # Type the trigger character-by-character so the suggestion service fires
    # the canned-response delimiter `::` lookup. Type `::` first, wait for the
    # fetch-canned-responses RPC to return, then type the filter 'hello'.
    page.keyboard.type("::", delay=100)
    page.wait_for_timeout(800)  # 250ms debounce + RPC round-trip
    page.keyboard.type("hello", delay=80)
    page.wait_for_timeout(800)

    # The NavigableList suggestion popover should now show the `hello`
    # canned response. Click the first item.
    popover = page.locator(
        ".o-mail-NavigableList-item:has-text('hello'), "
        ".o-mail-NavigableList .o-mail-NavigableList-item"
    ).first
    popover.wait_for(state="visible", timeout=5000)
    popover.click()
    page.wait_for_timeout(400)

    # Sanity check: the composer text should now be the substitution (plus a
    # trailing space that Odoo inserts after a canned response).
    value = textarea.evaluate("el => el.value || el.textContent")
    if EXPECTED_REPLY not in (value or ""):
        raise RuntimeError(
            f"Canned-response substitution did not land in composer: "
            f"{value!r}"
        )

    # Send via Enter (Discuss textarea default) so we trigger the same flow a
    # browser-use agent would.
    textarea.press("Enter")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Wait for the message to appear in the thread.
    page.locator(
        f".o-mail-Message-body:has-text('{EXPECTED_REPLY}')"
    ).first.wait_for(state="visible", timeout=10000)


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    _open_livechat_session(page)
    _fire_canned_response(page)


run_oracle(oracle)
