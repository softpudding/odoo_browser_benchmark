"""Oracle for account.create_vendor_bill_confirm.

Navigate to vendor bills, create a new bill for Meridian Supply Co with
2 product lines, set bill date and reference, then confirm.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_date,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/vendor-bills")
    _wait_no_loading(page)

    # Create new vendor bill
    click_create(page)
    page.wait_for_timeout(500)

    # Set vendor
    set_many2one(page, "partner_id", "Meridian Supply Co")
    page.wait_for_timeout(500)

    # Set bill reference
    fill_field(page, "ref", "MSC-INV-4421")
    page.wait_for_timeout(500)

    # Set bill date
    set_date(page, "invoice_date", "05/01/2026")
    page.wait_for_timeout(500)

    # Add first line: Cable Tray × 100 @ 12.50
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 0, "product_id", "Cable Tray")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "quantity", "100")
    page.wait_for_timeout(300)
    set_o2m_field(page, 0, "price_unit", "12.50")
    page.wait_for_timeout(500)

    # Add second line: Junction Box × 50 @ 8.00
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 1, "product_id", "Junction Box")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "quantity", "50")
    page.wait_for_timeout(300)
    set_o2m_field(page, 1, "price_unit", "8.00")
    page.wait_for_timeout(500)

    # Confirm the bill
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
