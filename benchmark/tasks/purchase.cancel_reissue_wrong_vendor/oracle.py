"""Oracle for purchase.cancel_reissue_wrong_vendor.

Find confirmed PO from Atlas Industrial with origin VENDOR-FIX-01.
Cancel it, then create a new PO for Pinnacle Parts with the same lines:
  - Hydraulic Pump: qty 5, price 340
  - Pressure Gauge: qty 10, price 85
Confirm the new PO.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_button,
    click_create,
    click_list_row,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    # Find and open the PO from Atlas Industrial with origin VENDOR-FIX-01
    click_list_row(page, "VENDOR-FIX-01")
    page.wait_for_timeout(1000)

    # Cancel the PO
    click_button(page, "Cancel")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Confirm cancellation if a dialog appears
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Ok'), button:has-text('Confirm'), button.btn-primary").first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Go back to purchase orders list
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    # Create new PO
    click_create(page)
    page.wait_for_timeout(1000)

    # Set vendor to Pinnacle Parts
    set_many2one(page, "partner_id", "Pinnacle Parts")
    page.wait_for_timeout(500)

    # Add first line: Hydraulic Pump, qty 5, price 340
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 0, "product_id", "Hydraulic Pump")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "product_qty", "5")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "price_unit", "340")
    page.wait_for_timeout(500)

    # Add second line: Pressure Gauge, qty 10, price 85
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 1, "product_id", "Pressure Gauge")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "product_qty", "10")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "price_unit", "85")
    page.wait_for_timeout(500)

    # Confirm the new PO
    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Handle any confirmation dialog
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Ok'), button.btn-primary").first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
