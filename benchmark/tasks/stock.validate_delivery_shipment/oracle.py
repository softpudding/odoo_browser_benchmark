"""Oracle for stock.validate_delivery_shipment.

Go to Inventory, open delivery BENCH-DEL-01, set partial done quantities on
its two move lines (12 and 5), click Validate, then choose No Backorder.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    click_status_button,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Click the Delivery Orders card on the inventory dashboard
    cards = page.locator(".o_kanban_record:visible")
    opened = False
    for i in range(cards.count()):
        card = cards.nth(i)
        if "Delivery Orders" in card.inner_text() or "Delivery Order" in card.inner_text():
            card.click()
            opened = True
            break
    if not opened:
        page.locator(
            ".o_kanban_record:has-text('Delivery'):visible"
        ).first.click()
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Ensure list view + find BENCH-DEL-01
    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(400)
    click_list_row(page, "BENCH-DEL-01")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Set done quantities on each move line
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    for i in range(rows.count()):
        row_text = rows.nth(i).inner_text()
        if "Steel Bracket" in row_text:
            set_o2m_field(page, i, "quantity", "12")
            page.wait_for_timeout(300)
        elif "Copper Wire" in row_text:
            set_o2m_field(page, i, "quantity", "5")
            page.wait_for_timeout(300)
    page.wait_for_timeout(500)

    # Click Validate
    click_status_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Backorder dialog should appear: explicitly choose No Backorder
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        no_bo = modal.last.locator("button:has-text('No Backorder')")
        if no_bo.count() > 0:
            no_bo.first.click()
        else:
            modal.last.locator(
                "button:has-text('Apply'), "
                "button:has-text('Validate'), "
                "button:has-text('Ok'), "
                "button.btn-primary"
            ).first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
