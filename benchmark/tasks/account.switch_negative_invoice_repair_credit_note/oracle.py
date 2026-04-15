"""Oracle for account.switch_negative_invoice_repair_credit_note.

Open draft invoice with origin RET-508 (negative total) for Lumen Works,
switch to credit note via Action menu, fix lines per known correct values,
set Customer Reference, and post.

Lines (from seed.py):
  Row 0: Return Fee           - should be Qty=1, Discount=0  (seeded as 1, 0)
  Row 1: Service Retainer     - should be Qty=2, Discount=10 (seeded as 3, 0)
  Row 2: Restocking Surcharge - should be Qty=1, Discount=5  (seeded as 1, 15)
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Click the draft invoice by its origin
    click_list_row(page, "RET-508")
    page.wait_for_timeout(1000)

    # Use Action menu to switch to credit note
    page.locator(".o_cp_action_menus .dropdown-toggle").first.click()
    page.wait_for_timeout(500)
    page.locator(
        ".o_cp_action_menus .dropdown-menu .dropdown-item"
    ).filter(has_text="Credit Note").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Fix line 0: Return Fee - Qty=1, Discount=0 (already correct, but set anyway)
    set_o2m_field(page, 0, "quantity", "1")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "discount", "0")
    page.wait_for_timeout(500)

    # Fix line 1: Service Retainer - Qty=2, Discount=10
    set_o2m_field(page, 1, "quantity", "2")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "discount", "10")
    page.wait_for_timeout(500)

    # Fix line 2: Restocking Surcharge - Qty=1, Discount=5
    set_o2m_field(page, 2, "quantity", "1")
    page.wait_for_timeout(500)
    set_o2m_field(page, 2, "discount", "5")
    page.wait_for_timeout(500)

    # Go to Other Info tab and set Customer Reference
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "ref", "RET-508-READY")
    page.wait_for_timeout(500)

    # Post the credit note
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
