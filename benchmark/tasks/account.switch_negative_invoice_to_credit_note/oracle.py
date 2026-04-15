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
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Click the draft invoice by its origin
    click_list_row(page, "RET-204")
    page.wait_for_timeout(1000)

    # Use Action menu to switch to credit note
    page.locator(".o_cp_action_menus .dropdown-toggle").first.click()
    page.wait_for_timeout(500)
    page.locator(
        ".o_cp_action_menus .dropdown-menu .dropdown-item"
    ).filter(has_text="Credit Note").first.click()
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
