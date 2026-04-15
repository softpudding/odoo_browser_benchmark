"""Oracle for account.repair_and_post_invoice.

Open draft invoice with origin APR-OPS for Beacon Design, fix quantity and
discount on each line per the known correct values, set Customer Reference,
and post.

Lines (from seed.py):
  Row 0: Acoustic Panel  - should be Qty=2, Discount=5  (seeded as 1, 0)
  Row 1: Focus Lamp      - should be Qty=1, Discount=15 (seeded as 3, 0)
  Row 2: Desk Shelf      - should be Qty=3, Discount=0  (seeded as 1, 10)
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
    click_list_row(page, "APR-OPS")
    page.wait_for_timeout(1000)

    # Fix line 0: Acoustic Panel - Qty=2, Discount=5
    set_o2m_field(page, 0, "quantity", "2")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "discount", "5")
    page.wait_for_timeout(500)

    # Fix line 1: Focus Lamp - Qty=1, Discount=15
    set_o2m_field(page, 1, "quantity", "1")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "discount", "15")
    page.wait_for_timeout(500)

    # Fix line 2: Desk Shelf - Qty=3, Discount=0
    set_o2m_field(page, 2, "quantity", "3")
    page.wait_for_timeout(500)
    set_o2m_field(page, 2, "discount", "0")
    page.wait_for_timeout(500)

    # Go to Other Info tab and set Customer Reference
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "ref", "APR-OPS-READY")
    page.wait_for_timeout(500)

    # Post the invoice
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
