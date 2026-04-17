"""Oracle for purchase.create_rfq_confirm_receive_backorder.

Create a new RFQ for Summit Ridge Components with 3 product lines,
confirm the order, navigate to the receipt, set partial done quantities,
validate, and create a backorder for the remaining quantities.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    click_stat_button,
    click_status_button,
    fill_field,
    login,
    modal_click_button,
    navigate,
    run_oracle,
    set_date,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


LINES = [
    ("Hydraulic Cylinder 50mm", "20", "85"),
    ("Pressure Gauge PSI", "30", "24.50"),
    ("Flow Control Valve", "15", "112"),
]

DONE_QTYS = [
    ("Hydraulic Cylinder 50mm", "12"),
    ("Pressure Gauge PSI", "30"),
    ("Flow Control Valve", "8"),
]


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    # Create new RFQ
    click_create(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Set vendor
    set_many2one(page, "partner_id", "Summit Ridge Components")
    page.wait_for_timeout(800)

    # Set Order Deadline (date_order)
    set_date(page, "date_order", "06/20/2026")
    page.wait_for_timeout(500)

    # Set Vendor Reference
    fill_field(page, "partner_ref", "SRC-PO-2026-Q2")
    page.wait_for_timeout(500)

    # Add 3 product lines
    for i, (product, qty, price) in enumerate(LINES):
        click_add_a_line(page)
        page.wait_for_timeout(500)
        set_o2m_many2one(page, i, "product_id", product)
        page.wait_for_timeout(500)
        set_o2m_field(page, i, "product_qty", qty)
        page.wait_for_timeout(300)
        set_o2m_field(page, i, "price_unit", price)
        page.wait_for_timeout(300)

    # Confirm Order
    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Handle any confirmation modal (e.g. "This vendor is not available")
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button.btn-primary").first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Click the Receipt smart button
    click_stat_button(page, "Receipt")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Set done quantities on each move line
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    page.wait_for_timeout(500)
    for i in range(rows.count()):
        row_text = rows.nth(i).inner_text()
        for product_name, done_qty in DONE_QTYS:
            if product_name in row_text:
                set_o2m_field(page, i, "quantity", done_qty)
                page.wait_for_timeout(400)
                break

    page.wait_for_timeout(500)

    # Click Validate
    click_status_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # In the backorder dialog, click "Create Backorder"
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Create Backorder')").first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
