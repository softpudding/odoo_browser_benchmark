"""Oracle for sale.add_note_to_quotation.

Open draft quotation BENCH-NOTE-01, post an internal log note with exact text.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the draft quotation BENCH-NOTE-01
    click_list_row(page, "BENCH-NOTE-01")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Scroll to chatter area
    chatter = page.locator("#chatter").first
    chatter.scroll_into_view_if_needed()
    page.wait_for_timeout(500)

    # Click Log note tab
    page.get_by_role("tab", name="Log note").click()
    page.wait_for_timeout(500)

    # Type the note
    chatter_editor = chatter.locator(".o-mail-Chatter-composer").first
    chatter_editor.fill("Customer requested delivery by May 1, 2026. Please coordinate with warehouse.")
    page.wait_for_timeout(500)

    # Click Log button
    page.get_by_role("button", name="Log").click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)