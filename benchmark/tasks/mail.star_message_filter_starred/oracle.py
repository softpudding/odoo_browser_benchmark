"""Oracle for mail.star_message_filter_starred.

Navigate to the Administrator partner record, find the target message
in the chatter, and star (bookmark) it.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Clear filters.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break

    # Search for Administrator partner.
    search_input = page.locator(".o_searchview input:visible").first
    search_input.click()
    search_input.fill("Administrator")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Open the partner card.
    card = page.locator(
        ".o_kanban_record:has-text('Administrator'):visible, "
        ".o_data_row:has-text('Administrator'):visible"
    ).first
    card.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Scroll to the chatter.
    chatter = page.locator(".o-mail-Chatter, .o_chatter").first
    chatter.scroll_into_view_if_needed()
    page.wait_for_timeout(500)

    # Find the target message and star it.
    msg = page.locator(
        ".o-mail-Message:has-text('Finance close blocker')"
    ).first
    msg.wait_for(state="visible", timeout=15000)
    msg.hover()
    page.wait_for_timeout(500)
    star_btn = page.locator(
        ".o-mail-Message:has-text('Finance close blocker') "
        "button[title*='star' i], "
        ".o-mail-Message:has-text('Finance close blocker') "
        "button[title*='Bookmark' i], "
        ".o-mail-Message:has-text('Finance close blocker') "
        "button[title*='Mark as Todo' i]"
    ).first
    star_btn.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
