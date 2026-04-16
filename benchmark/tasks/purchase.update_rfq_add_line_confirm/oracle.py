"""Oracle for purchase.update_rfq_add_line_confirm.

Find draft RFQ BENCH-RFQ-UPD for Pinnacle Hardware. Add a new product
line (Hex Wrench Set × 25 @ $15.00), change order deadline to 05/20/2026,
and confirm.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    set_date,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    # Find and open the RFQ
    click_list_row(page, "BENCH-RFQ-UPD")
    page.wait_for_timeout(500)

    # Add new product line: Hex Wrench Set × 25 @ 15.00
    click_add_a_line(page)
    page.wait_for_timeout(500)

    # The new line is the 3rd row (index 2) since there are 2 existing lines
    set_o2m_many2one(page, 2, "product_id", "Hex Wrench Set")
    page.wait_for_timeout(500)
    set_o2m_field(page, 2, "product_qty", "25")
    page.wait_for_timeout(300)
    set_o2m_field(page, 2, "price_unit", "15.00")
    page.wait_for_timeout(500)

    # Change order deadline
    set_date(page, "date_order", "05/20/2026")
    page.wait_for_timeout(500)

    # Confirm the order
    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Handle any confirmation dialog
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        ok_btn = modal.last.locator(
            "button:has-text('Ok'), button:has-text('Confirm'), "
            "button.btn-primary"
        )
        if ok_btn.count() > 0:
            ok_btn.first.click()
            page.wait_for_timeout(500)
            _wait_no_loading(page)


run_oracle(oracle)
