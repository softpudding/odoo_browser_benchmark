"""Oracle for purchase_stock.receive_partial_scrap_damaged_units."""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    click_stat_button,
    login,
    modal_fill_field,
    modal_set_many2one,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def _set_done_qty(page, row_index, value):
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row, "
        ".o_list_view .o_data_row"
    ).nth(row_index)
    cell = row.locator("td[name='quantity'], .o_field_widget[name='quantity']").first
    cell.click()
    page.wait_for_timeout(300)
    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "SCRAP-PO-07")
    page.wait_for_timeout(1000)

    receive_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Receive'), "
        "button[name='action_view_picking']:visible"
    ).first
    receive_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    _set_done_qty(page, 0, "4")
    _set_done_qty(page, 1, "7")

    click_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Create Backorder')").first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)
        _wait_for_ready(page)

    action_menu = page.locator(".o_cp_action_menus .dropdown-toggle:visible").last
    action_menu.click()
    page.wait_for_timeout(500)
    page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Scrap'), "
        ".o-dropdown--menu:visible .dropdown-item:has-text('Scrap')"
    ).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    modal_set_many2one(page, "product_id", "Bench Filter Cartridge")
    modal_fill_field(page, "scrap_qty", "1")
    scrap_btn = page.locator(
        ".modal:visible button[name='action_validate']:visible, "
        ".modal:visible button:has-text('Scrap Products'):visible, "
        ".modal:visible .modal-footer button.btn-primary:visible"
    ).first
    scrap_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)
    click_list_row(page, "SCRAP-PO-07")
    page.wait_for_timeout(1000)
    click_stat_button(page, "Receipt")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    ready_row = page.locator(
        ".o_list_view .o_data_row:has-text('Ready'), "
        ".o_list_view .o_data_row:has-text('Assigned')"
    )
    if ready_row.count() > 0:
        ready_row.first.click()
    else:
        rows = page.locator(".o_list_view .o_data_row")
        rows.nth(1).click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    _set_done_qty(page, 0, "2")
    _set_done_qty(page, 1, "3")

    click_button(page, "Validate")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Ok'), button.btn-primary").first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
