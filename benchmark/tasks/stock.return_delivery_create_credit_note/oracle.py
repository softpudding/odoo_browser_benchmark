"""Oracle for stock.return_delivery_create_credit_note.

Navigate to Inventory, open delivery BENCH-DEL-RET, create a partial return
(4x Industrial Fan Unit only), validate the return, then navigate to the
Sales Order, open the posted invoice, create a credit note with reason and
date, and confirm it.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    click_stat_button,
    click_status_button,
    click_tab,
    ensure_list_view,
    login,
    modal_click_button,
    modal_fill_field,
    modal_set_date,
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
    page.wait_for_timeout(800)

    # ── Step 1: Open Delivery Orders from the inventory dashboard ──
    cards = page.locator(".o_kanban_record:visible")
    opened = False
    for i in range(cards.count()):
        card = cards.nth(i)
        if "Delivery Orders" in card.inner_text() or "Delivery Order" in card.inner_text():
            card.click()
            opened = True
            break
    if not opened:
        page.locator(".o_kanban_record:has-text('Delivery'):visible").first.click()
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # ── Step 2: Find and open delivery BENCH-DEL-RET ──
    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(400)
    click_list_row(page, "BENCH-DEL-RET")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # ── Step 3: Click Return button ──
    click_status_button(page, "Return")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # ── Step 4: Edit return quantities in the wizard modal ──
    page.wait_for_selector(".modal:visible", timeout=10000)
    modal = page.locator(".modal:visible").last
    rows = modal.locator(".o_data_row")
    page.wait_for_timeout(500)

    for i in range(rows.count()):
        row = rows.nth(i)
        product_text = row.inner_text()
        if "Industrial Fan Unit" in product_text:
            qty_cell = row.locator("td[name='quantity']")
            qty_cell.click()
            page.wait_for_timeout(300)
            inp = qty_cell.locator("input").first
            inp.fill("4")
            inp.press("Tab")
            page.wait_for_timeout(300)
        elif "Rubber Gasket Set" in product_text:
            qty_cell = row.locator("td[name='quantity']")
            qty_cell.click()
            page.wait_for_timeout(300)
            inp = qty_cell.locator("input").first
            inp.fill("0")
            inp.press("Tab")
            page.wait_for_timeout(300)

    page.wait_for_timeout(500)

    # Click Return in the wizard
    modal_click_button(page, "Return")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # ── Step 5: On the return picking, set Done qty and Validate ──
    # We should now be on the return picking form.
    # Set done quantity for Industrial Fan Unit to 4.
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    page.wait_for_timeout(500)
    for i in range(rows.count()):
        row_text = rows.nth(i).inner_text()
        if "Industrial Fan Unit" in row_text:
            set_o2m_field(page, i, "quantity", "4")
            page.wait_for_timeout(300)
            break

    page.wait_for_timeout(500)

    # Click Validate
    click_status_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Handle any backorder / confirmation dialog
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal_text = modal.last.inner_text()
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

    # ── Step 6: Navigate to the Sales Order ──
    # Go to the Sales app and find the SO with client_order_ref BENCH-DEL-RET
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(400)
    click_list_row(page, "BENCH-DEL-RET")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # ── Step 7: Click Invoices smart button ──
    click_stat_button(page, "Invoice")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # We may land on a list of invoices or directly on the invoice.
    # If on a list, click the posted invoice.
    invoice_list = page.locator(".o_list_view .o_data_row")
    if invoice_list.count() > 0:
        # Click the first (posted) invoice
        invoice_list.first.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
        page.wait_for_timeout(800)

    # ── Step 8: Click Credit Note button ──
    click_status_button(page, "Credit Note")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # ── Step 9: Fill the credit note wizard ──
    page.wait_for_selector(".modal:visible", timeout=10000)

    modal_fill_field(page, "reason", "Partial return - defective units")
    page.wait_for_timeout(500)

    # Set the credit note date to 06/08/2026
    modal_set_date(page, "date", "06/08/2026")
    page.wait_for_timeout(500)

    # Click Reverse
    modal_click_button(page, "Reverse")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # ── Step 10: Confirm (post) the draft credit note ──
    # When the credit note date is in the future, Odoo 19 may set auto_post='at_date'
    # which hides the Confirm button. Set auto_post to 'No' first if needed.
    confirm_btn = page.locator(".o_statusbar_buttons button:visible:has-text('Confirm')")
    if confirm_btn.count() == 0:
        # Need to change auto_post to No
        click_tab(page, "Other Info")
        page.wait_for_timeout(500)

        auto_post_widget = page.locator(".o_field_widget[name='auto_post']").first
        auto_post_widget.locator(".o_select_menu, .dropdown-toggle").first.click()
        page.wait_for_timeout(500)
        options = page.locator(
            ".dropdown-menu:visible .o_select_menu_item, "
            ".dropdown-menu:visible .dropdown-item"
        )
        for i in range(options.count()):
            if options.nth(i).inner_text().strip() == "No":
                options.nth(i).click()
                break
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
