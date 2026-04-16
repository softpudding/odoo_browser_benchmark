"""Oracle for purchase.new_rfq_three_lines_date.

Create a new RFQ for vendor Meridian Supply Co with:
- Order Deadline: 05/30/2026
- 3 product lines: Rubber Gasket 200×$1.50, Stainless Bolt M8 500×$0.75, Hex Nut M8 500×$0.40
Then confirm the order.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    login,
    navigate,
    run_oracle,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


LINES = [
    ("Rubber Gasket", "200", "1.50"),
    ("Stainless Bolt M8", "500", "0.75"),
    ("Hex Nut M8", "500", "0.40"),
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
    set_many2one(page, "partner_id", "Meridian Supply Co")
    page.wait_for_timeout(800)

    # Set Order Deadline — date_order uses a calendar datepicker in Odoo 19.
    # Must click Next to navigate from current month to May 2026, then click day 30.
    date_widget = page.locator(".o_field_widget[name='date_order']").first
    date_btn = date_widget.locator("button").first
    date_btn.click()
    page.wait_for_timeout(500)
    # Navigate forward until we reach May 2026
    for _ in range(12):
        header = page.locator(".o_datetime_picker .o_header_part:visible").first
        if "May 2026" in header.inner_text():
            break
        page.locator(".o_datetime_picker .o_next:visible").first.click()
        page.wait_for_timeout(200)
    # Click on day 30 of the current month (exclude out-of-range overflow cells)
    cell_30 = page.locator(
        ".o_datetime_picker .o_date_item_cell:visible:not(.o_out_of_range)"
    ).filter(has_text="30")
    cell_30.first.click()
    page.wait_for_timeout(300)
    # Click Apply to confirm
    apply_btn = page.locator(".o_datetime_picker .o_apply:visible")
    if apply_btn.count() > 0:
        apply_btn.first.click()
        page.wait_for_timeout(300)
    page.wait_for_timeout(300)

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
    confirm_btn = page.locator(
        "button[name='button_confirm']:visible, "
        "button:has-text('Confirm Order'):visible"
    ).first
    confirm_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Handle any confirmation modal
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button.btn-primary").first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
