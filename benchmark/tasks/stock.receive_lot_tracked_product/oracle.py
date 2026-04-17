"""Oracle for stock.receive_lot_tracked_product.

Open receipt BENCH-LOT-RCV-01, click the 'Details' button on the move
line to open the detail-operations popup, enter LOT-2026-R042 in the
lot field (creating the lot on the fly) — the seed already pre-fills
the done quantity — save/close the dialog, then Validate.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)

LOT_NAME = "LOT-2026-R042"
ORIGIN = "BENCH-LOT-RCV-01"


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    cards = page.locator(".o_kanban_record:visible")
    for i in range(cards.count()):
        if "Receipts" in cards.nth(i).inner_text():
            cards.nth(i).click()
            break
    _wait_no_loading(page)
    page.wait_for_timeout(700)

    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(300)

    click_list_row(page, ORIGIN)
    page.wait_for_timeout(900)
    _wait_no_loading(page)

    # Click "Details" button on the first move line.
    details = page.locator(
        "button[name='action_show_details']:visible"
    )
    details.first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    dialog = page.locator(".modal:visible").last

    # Inside the dialog, find the move.line list. For lot-tracked products
    # the dialog exposes a list of move lines with Lot/Serial and Quantity.
    # If no line exists yet, add one.
    ml_rows = dialog.locator(".o_data_row")
    if ml_rows.count() == 0:
        add_btn = dialog.locator(
            "a:has-text('Add a line'):visible, "
            "button:has-text('Add a line'):visible"
        )
        if add_btn.count() > 0:
            add_btn.first.click()
            page.wait_for_timeout(500)
            ml_rows = dialog.locator(".o_data_row")

    row = ml_rows.last
    # The lot cell — may be named lot_id or lot_name.
    lot_cell = row.locator(
        "div[name='lot_id']:visible, "
        "td[name='lot_id']:visible, "
        "div[name='lot_name']:visible, "
        "td[name='lot_name']:visible"
    ).first
    lot_cell.click()
    page.wait_for_timeout(300)

    # Type the lot name.
    inp = row.locator(
        "div[name='lot_id'] input:visible, "
        "div[name='lot_name'] input:visible"
    ).first
    if inp.count() == 0:
        inp = row.locator("input:visible").first
    inp.fill(LOT_NAME)
    page.wait_for_timeout(700)

    # Accept the "Create …" option from the dropdown or press Enter.
    create_opt = page.locator(
        f'.o-autocomplete--dropdown-item:has-text("Create"):visible'
    )
    if create_opt.count() > 0:
        create_opt.first.click()
    else:
        inp.press("Enter")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Make sure quantity is 20 (it should be from the seed pre-fill).
    qty_cell = row.locator(
        "div[name='quantity']:visible, td[name='quantity']:visible"
    ).first
    if qty_cell.count() > 0:
        current = (qty_cell.inner_text() or "").strip()
        if current not in ("20", "20.0", "20.00"):
            qty_cell.click()
            page.wait_for_timeout(200)
            qty_input = row.locator(
                "div[name='quantity'] input:visible"
            ).first
            if qty_input.count() > 0:
                qty_input.press("Control+A")
                qty_input.press("Meta+A")
                qty_input.fill("20")
                qty_input.press("Tab")
                page.wait_for_timeout(300)

    # Save/close the dialog.
    save_btn = dialog.locator(
        "button.btn-primary:has-text('Save'):visible, "
        "button.o_form_button_save:visible, "
        "button.btn-primary:visible"
    ).first
    save_btn.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Validate.
    click_status_button(page, "Validate")
    page.wait_for_timeout(1800)
    _wait_no_loading(page)

    # Handle confirmation popup, if any.
    for _ in range(2):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        btn = modal.last.locator(
            "button:has-text('Apply'):visible, "
            "button:has-text('Validate'):visible, "
            "button.btn-primary:visible"
        ).first
        if btn.count() > 0:
            btn.click()
            page.wait_for_timeout(1200)
            _wait_no_loading(page)
        else:
            break


run_oracle(oracle)
