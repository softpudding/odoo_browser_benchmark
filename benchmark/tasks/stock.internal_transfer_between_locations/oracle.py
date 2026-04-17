"""Oracle for stock.internal_transfer_between_locations.

Create a new Internal Transfer from WH/Stock to WH/Stock/Shelf A1,
add Benchmark Shelf Widget qty=5, validate.
"""

from benchmark.oracle_helpers import (
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    # Internal transfers by type — use the main warehouse's internal picking type.
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Click the Internal Transfers dashboard card.
    card = page.locator(
        ".o_kanban_record:has-text('Internal Transfers') button:has-text('New'):visible, "
        ".o_kanban_record:has-text('Internal Transfers') a:has-text('New'):visible"
    )
    if card.count() > 0:
        card.first.click()
    else:
        # Fallback: navigate to all transfers and filter internal.
        navigate(page, "/odoo/action-stock.stock_picking_action_picking_type")
        page.wait_for_timeout(800)
        card2 = page.locator(
            ".o_kanban_record:has-text('Internal Transfers') button:has-text('New'):visible, "
            ".o_kanban_record:has-text('Internal Transfers') a:has-text('New'):visible"
        )
        if card2.count() > 0:
            card2.first.click()
        else:
            # Last resort: open a generic new picking and set picking_type.
            new_btn = page.locator(".o_control_panel_main_buttons button:has-text('New'):visible")
            new_btn.first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Set source, destination, origin.
    set_many2one(page, "location_id", "WH/Stock")
    set_many2one(page, "location_dest_id", "WH/Stock/Shelf A1")
    fill_field(page, "origin", "BENCH-INT-SHELF-A1")

    # Add a move line: product + demand qty.
    add_line = page.locator(
        ".o_field_x2many[name='move_ids_without_package'] a.o_field_x2many_list_row_add:visible, "
        ".o_field_x2many[name='move_ids'] a.o_field_x2many_list_row_add:visible, "
        "a.o_field_x2many_list_row_add:visible"
    )
    add_line.first.click()
    page.wait_for_timeout(400)
    set_o2m_many2one(page, 0, "product_id", "Benchmark Shelf Widget")
    set_o2m_field(page, 0, "product_uom_qty", "5")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(800)

    # Confirm (if not auto) and validate.
    confirm_btn = page.locator(
        ".o_form_statusbar button[name='action_confirm']:visible"
    )
    if confirm_btn.count() > 0:
        confirm_btn.first.click()
        page.wait_for_timeout(800)

    # Set done quantity on the move line — open detailed operations if needed.
    # Easiest: set quantity column directly to 5.
    qty_input = page.locator(
        "td[name='quantity'] input:visible, "
        "input[name='quantity']:visible"
    )
    if qty_input.count() > 0:
        qty_input.first.click()
        qty_input.first.fill("5")
        page.keyboard.press("Tab")
        page.wait_for_timeout(300)

    # Validate.
    validate_btn = page.locator(
        ".o_form_statusbar button[name='button_validate']:visible, "
        ".o_form_statusbar button:has-text('Validate'):visible"
    )
    validate_btn.first.click()
    page.wait_for_timeout(1200)
    # Accept any confirmation modal (Apply / OK).
    ok = page.locator(
        ".modal button.btn-primary:visible, "
        ".modal button:has-text('Apply'):visible, "
        ".modal button:has-text('OK'):visible"
    )
    if ok.count() > 0:
        try:
            ok.first.click()
        except Exception:
            pass
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
