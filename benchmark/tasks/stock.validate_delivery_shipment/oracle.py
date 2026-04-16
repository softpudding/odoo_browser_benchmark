"""Oracle for stock.validate_delivery_shipment.

Go to Inventory, open delivery BENCH-DEL-01, set done quantities on
its two move lines (20 and 8), and click Validate.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)

    # Open Delivery Orders card
    delivery_card = page.locator(
        ".o_kanban_record:has-text('Delivery Orders'), "
        ".o_kanban_record:has-text('Delivery')"
    ).first
    delivery_card.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)

    click_list_row(page, "BENCH-DEL-01")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Set done quantities on each move line. In Odoo 19 the outgoing
    # delivery form uses a move list with a `quantity` column.
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    n = rows.count()
    for i in range(n):
        row_text = rows.nth(i).inner_text()
        if "Steel Bracket" in row_text:
            set_o2m_field(page, i, "quantity", "20")
        elif "Copper Wire" in row_text:
            set_o2m_field(page, i, "quantity", "8")
    page.wait_for_timeout(500)

    # Click Validate
    validate_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Validate'), "
        "button:visible:has-text('Validate')"
    ).first
    validate_btn.click()
    page.wait_for_timeout(1500)

    # If a backorder dialog appears, choose No Backorder
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        no_bo = modal.last.locator(
            "button:has-text('No Backorder')"
        )
        if no_bo.count() > 0:
            no_bo.first.click()
        else:
            modal.last.locator(
                "button:has-text('Apply'), "
                "button:has-text('Validate'), "
                "button:has-text('OK')"
            ).first.click()
        page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
