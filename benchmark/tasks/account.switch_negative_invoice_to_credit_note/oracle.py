"""Oracle for account.switch_negative_invoice_to_credit_note.

Open draft invoice with origin RET-204 (negative total) for Lumen Works,
switch to credit note via Action menu, set Customer Reference, and post.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def _click_action_menu_item(page, text):
    """Click an item in the Action menu (gear/cog icon).

    In Odoo 19, the dropdown items are NOT inside .o_cp_action_menus .dropdown-menu
    but appear as a general .dropdown-menu:visible attached to the body.
    """
    # Click the gear/cog toggle button
    toggle = page.locator(".o_cp_action_menus .dropdown-toggle:visible")
    if toggle.count() == 0:
        raise RuntimeError("Action menu toggle not found")

    toggle.first.click()
    page.wait_for_timeout(500)

    # Items appear in a generic .dropdown-menu:visible (NOT inside .o_cp_action_menus)
    items = page.locator(".dropdown-menu:visible .dropdown-item")
    for i in range(items.count()):
        item_text = items.nth(i).inner_text().strip()
        if text.lower() in item_text.lower():
            items.nth(i).click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)
            return True

    # Close the menu
    page.press("body", "Escape")
    page.wait_for_timeout(300)
    raise RuntimeError(f"Action menu item '{text}' not found")


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Click the draft invoice by its origin
    click_list_row(page, "RET-204")
    page.wait_for_timeout(1000)

    # Use Action menu to switch to credit note.
    # In Odoo 19, the item is "Switch into invoice/credit note"
    for label in ["Switch into", "Credit Note", "Switch to Credit Note", "Refund"]:
        try:
            _click_action_menu_item(page, label)
            break
        except RuntimeError:
            continue
    else:
        raise RuntimeError("Could not find credit note action in Action menu")

    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Go to Other Info tab and set Customer Reference
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "ref", "RET-204-REFUND")
    page.wait_for_timeout(500)

    # Post the credit note
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
