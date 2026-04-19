"""Oracle for stock.transfer_create_internal_transfer_validate.

Navigate to Inventory > Transfers filtered to Internal Transfers
(/odoo/inventory/internal — action `stock.action_picking_tree_internal`,
context `restricted_picking_type_code='internal'` so New creates an
internal picking). Click New, set Destination to WH/Stock/Shelf C, add
one Bench Move Item x5 line, click Mark as Todo (Confirm), then Validate.
Source auto-fills to WH/Stock because that is the internal picking type's
default_location_src_id on the base warehouse.
"""

from benchmark.oracle_helpers import (
    full_url,
    login,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


PRODUCT_NAME = "Bench Move Item"
LOCATION_SRC = "WH/Stock"
LOCATION_DEST = "WH/Stock/Shelf C"
SHELF_SEARCH = "Shelf C"
DEMAND_QTY = 5


def _set_m2o(page, widget, search_text, exact_text):
    """Pick an exact-match autocomplete suggestion on a many2one input."""
    inp = widget.locator("input:visible").first
    inp.click()
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(1000)
    dropdown_items = page.locator(
        ".dropdown-menu .dropdown-item:visible, "
        ".o-autocomplete--dropdown-item:visible"
    )
    matched = None
    n = dropdown_items.count()
    for i in range(n):
        item = dropdown_items.nth(i)
        text = item.inner_text().strip()
        if text == exact_text:
            matched = item
            break
    if matched is None:
        for i in range(n):
            item = dropdown_items.nth(i)
            text = item.inner_text().strip()
            if text.startswith(exact_text):
                matched = item
                break
    if matched is None:
        for i in range(n):
            item = dropdown_items.nth(i)
            text = item.inner_text().strip()
            if (
                search_text in text
                and "Search" not in text
                and "Create" not in text
                and "View" not in text
            ):
                matched = item
                break
    if matched is None:
        raise RuntimeError(
            f"No dropdown match for widget search={search_text!r} "
            f"exact={exact_text!r}"
        )
    matched.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _open_new_internal_transfer(page):
    # Navigate directly to the Internal Transfers list action. The URL
    # path 'internal' resolves to action_picking_tree_internal whose
    # context pins restricted_picking_type_code='internal', so clicking
    # New creates a draft internal picking with picking_type_id already
    # set to the warehouse's int_type_id (location_id + location_dest_id
    # default to that picking type's configured defaults — typically
    # WH/Stock → WH/Stock or similar).
    page.goto(full_url("/odoo/inventory/internal"), timeout=120000)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)


def _set_location(page, field_name, search_text, exact_text):
    widget = page.locator(
        f".o_form_view .o_field_widget[name='{field_name}']"
    ).first
    widget.wait_for(state="visible", timeout=15000)
    _set_m2o(page, widget, search_text, exact_text)


def _add_move_line(page):
    """Add a single move line in the Operations (move_ids_without_package)
    tab: product=Bench Move Item, demand=5."""
    # The Operations tab is the default on a draft picking; the
    # move_ids_without_package editable list is at the top of the form's
    # first notebook page. Click its "Add a line" button.
    # Notebook tab: Operations (the detailed moves tab).
    ops_tab = page.locator(
        ".o_notebook .nav-link:has-text('Operations'):visible"
    )
    if ops_tab.count() > 0:
        try:
            ops_tab.first.click()
            page.wait_for_timeout(500)
        except Exception:
            pass
    _wait_no_loading(page)

    # Find the Add a line button *inside* the move_ids_without_package
    # list (not the Additional Info or Detailed Operations lists).
    add_line = page.locator(
        ".o_field_x2many[name='move_ids_without_package'] "
        ".o_field_x2many_list_row_add a:visible, "
        ".o_field_one2many[name='move_ids_without_package'] "
        ".o_field_x2many_list_row_add a:visible"
    )
    if add_line.count() == 0:
        # Fallback to any "Add a line" link (form may have only one list).
        add_line = page.locator(
            ".o_field_x2many_list_row_add a:visible, "
            "a:has-text('Add a line'):visible"
        )
    add_line.first.click()
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    row = page.locator(".o_data_row.o_selected_row").first
    row.wait_for(state="visible", timeout=10000)

    # Fill Product (product_id) m2o.
    prod_cell = row.locator(
        "td[name='product_id'], .o_field_widget[name='product_id']"
    ).first
    prod_cell.click()
    page.wait_for_timeout(300)
    _set_m2o(page, prod_cell, PRODUCT_NAME, PRODUCT_NAME)

    # Fill Demand (product_uom_qty). The column may be labelled Demand.
    qty_cell = row.locator(
        "td[name='product_uom_qty'], .o_field_widget[name='product_uom_qty']"
    ).first
    qty_cell.click()
    page.wait_for_timeout(300)
    qty_input = row.locator(
        "td[name='product_uom_qty'] input:visible, "
        ".o_field_widget[name='product_uom_qty'] input:visible"
    ).first
    if qty_input.count() == 0:
        qty_input = row.locator("input:visible").first
    qty_input.press("Control+A")
    qty_input.press("Meta+A")
    qty_input.fill(str(DEMAND_QTY))
    qty_input.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _click_mark_as_todo(page):
    """Click the Mark as Todo / Confirm button to confirm + reserve."""
    btn = page.locator(
        ".o_form_statusbar button[name='action_confirm']:visible, "
        ".o_form_statusbar button:has-text('Mark as Todo'):visible, "
        ".o_form_statusbar button:has-text('Confirm'):visible"
    ).first
    btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)


def _click_validate(page):
    btn = page.locator(
        ".o_form_statusbar button[name='button_validate']:visible, "
        ".o_form_statusbar button:has-text('Validate'):visible"
    ).first
    btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Handle any confirmation modal (no backorder expected at full qty,
    # but a transient Apply / Ok modal may appear on some flows).
    for _ in range(3):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        m = modal.last
        btn = m.locator(
            "button:has-text('Apply'):visible, "
            "button:has-text('Validate'):visible, "
            "button:has-text('Ok'):visible, "
            "button.btn-primary:visible"
        ).first
        if btn.count() > 0:
            btn.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
        else:
            break


def oracle(page):
    login(page)

    _open_new_internal_transfer(page)

    # Ensure destination is the shelf sub-location (not the default
    # WH/Stock). The picking type defaults both source and dest to
    # WH/Stock — we only need to override the dest.
    _set_location(
        page, "location_dest_id", SHELF_SEARCH, LOCATION_DEST
    )

    # Ensure source is explicitly WH/Stock (it should already be).
    _set_location(page, "location_id", LOCATION_SRC, LOCATION_SRC)

    _add_move_line(page)

    # Save the draft picking so action_confirm has a persisted record.
    save_btn = page.locator(
        ".o_form_button_save:visible, "
        ".o_control_panel_main_buttons button:has-text('Save'):visible"
    )
    if save_btn.count() > 0:
        try:
            save_btn.first.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)
        except Exception:
            pass

    _click_mark_as_todo(page)
    _click_validate(page)


run_oracle(oracle)
