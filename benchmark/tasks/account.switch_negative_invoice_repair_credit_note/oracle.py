"""Oracle for account.switch_negative_invoice_repair_credit_note.

Open draft invoice with origin RET-508 (negative total) for Lumen Works,
switch to credit note via Action menu, fix lines per known correct values,
set Customer Reference, and post.

Lines (from seed.py, prices are negative on the invoice):
  Row 0: Return Fee           - should be Qty=1, Discount=0, Price=120  (seeded as 1, -120, 0)
  Row 1: Service Retainer     - should be Qty=2, Discount=10, Price=80  (seeded as 3, -80, 0)
  Row 2: Restocking Surcharge - should be Qty=1, Discount=5, Price=60   (seeded as 1, -60, 15)

After switching to credit note, prices remain negative and must be fixed to positive.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    click_status_button,
    enable_optional_column,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
    _dismiss_tooltips,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Click the draft invoice by its origin
    click_list_row(page, "RET-508")
    page.wait_for_timeout(1000)

    # Use Action menu to switch to credit note
    # In Odoo 19, the item is "Switch into invoice/credit note"
    toggle = page.locator(".o_cp_action_menus .dropdown-toggle:visible")
    toggle.first.click()
    page.wait_for_timeout(500)

    items = page.locator(".dropdown-menu:visible .dropdown-item")
    clicked = False
    for i in range(items.count()):
        item_text = items.nth(i).inner_text().strip()
        if "switch" in item_text.lower():
            items.nth(i).click()
            clicked = True
            break

    if not clicked:
        raise RuntimeError("Switch action not found in Action menu")

    # Wait for the switch to complete
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Enable the Disc.% optional column so we can edit discounts
    enable_optional_column(page, "Disc")
    page.wait_for_timeout(500)

    # After switching to credit note, prices remain negative.
    # Fix all line values: qty, price (positive), and discount.

    # Fix line 0: Return Fee - Qty=1, Price=120, Discount=0
    set_o2m_field(page, 0, "quantity", "1")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "price_unit", "120")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "discount", "0")
    page.wait_for_timeout(500)

    # Fix line 1: Service Retainer - Qty=2, Price=80, Discount=10
    set_o2m_field(page, 1, "quantity", "2")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "price_unit", "80")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "discount", "10")
    page.wait_for_timeout(500)

    # Fix line 2: Restocking Surcharge - Qty=1, Price=60, Discount=5
    set_o2m_field(page, 2, "quantity", "1")
    page.wait_for_timeout(500)
    set_o2m_field(page, 2, "price_unit", "60")
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

    # Handle any confirmation dialog that might appear
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Ok'), button:has-text('Confirm'), button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
