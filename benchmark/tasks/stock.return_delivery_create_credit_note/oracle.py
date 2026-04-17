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
    full_url,
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

    # Navigate directly to delivery orders list
    page.goto(full_url("/odoo/inventory/deliveries"), timeout=120000)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # ── Step 1–2: Find and open delivery BENCH-DEL-RET ──
    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(400)

    # Search for the origin in the search bar
    from benchmark.oracle_helpers import search_for
    search_for(page, "BENCH-DEL-RET")
    page.wait_for_timeout(500)

    # We may see both BENCH-DEL-RET and BENCH-DEL-RET-DIST.
    # Find the row whose origin cell is exactly "BENCH-DEL-RET" (partner Cascade Dynamics).
    rows = page.locator(".o_list_view .o_data_row")
    clicked = False
    for i in range(rows.count()):
        row = rows.nth(i)
        origin_cell = row.locator("td[name='origin']")
        if origin_cell.count() > 0:
            origin_text = origin_cell.first.inner_text().strip()
            if origin_text == "BENCH-DEL-RET":
                row.click()
                clicked = True
                break
    if not clicked:
        # Fallback: click any row with Cascade Dynamics
        row = page.locator(".o_list_view .o_data_row:has-text('Cascade Dynamics')").first
        row.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(800)

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
    page.goto(full_url("/odoo/sales"), timeout=120000)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(400)
    click_list_row(page, "Cascade Dynamics")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # ── Step 7: Click Invoices smart button ──
    click_stat_button(page, "Invoices")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # We may land on a list of invoices or directly on the invoice form.
    # If on a list, click the posted invoice.
    page.wait_for_timeout(1000)
    invoice_list = page.locator(".o_list_view .o_data_row")
    if invoice_list.count() > 0:
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

    # ── Step 9b: Edit the draft credit note lines to match the return ──
    # The reversal creates a full copy; we need to adjust to 4x Fan Unit only.
    # First, find and edit the Industrial Fan Unit line to qty 4
    click_tab(page, "Invoice Lines")
    page.wait_for_timeout(500)

    inv_rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    for i in range(inv_rows.count()):
        row_text = inv_rows.nth(i).inner_text()
        if "Industrial Fan Unit" in row_text:
            set_o2m_field(page, i, "quantity", "4")
            page.wait_for_timeout(300)

    # Delete the Rubber Gasket Set line
    for i in range(inv_rows.count()):
        row_text = inv_rows.nth(i).inner_text()
        if "Rubber Gasket Set" in row_text:
            # Click the row to select it, then delete
            inv_rows.nth(i).locator("td").first.click()
            page.wait_for_timeout(300)
            # Use the trash/delete icon on the row
            delete_btn = inv_rows.nth(i).locator(".o_list_record_remove, .fa-trash-o, button.o_list_record_remove")
            if delete_btn.count() > 0:
                delete_btn.first.click()
                page.wait_for_timeout(500)
            break

    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # ── Step 10: Handle auto_post and Confirm the credit note ──
    # When the credit note date is in the future, Odoo 19 sets auto_post='at_date'
    # which hides the Confirm button. Change auto_post to 'No' first.
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)

    auto_post_widget = page.locator(".o_field_widget[name='auto_post']").first
    if auto_post_widget.count() > 0 and auto_post_widget.first.is_visible():
        toggle = auto_post_widget.locator(
            ".o_select_menu_toggler, .o_select_menu, .dropdown-toggle, select"
        )
        if toggle.count() > 0:
            # Check if it's a <select> or a SelectMenu widget
            sel = auto_post_widget.locator("select")
            if sel.count() > 0:
                sel.first.select_option(label="No")
            else:
                toggle.first.click()
                page.wait_for_timeout(500)
                options = page.locator(
                    ".dropdown-menu:visible .o_select_menu_item, "
                    ".dropdown-menu:visible .dropdown-item, "
                    ".o_select_menu_menu:visible .o_select_menu_item"
                )
                for idx in range(options.count()):
                    if options.nth(idx).inner_text().strip() == "No":
                        options.nth(idx).click()
                        break
            page.wait_for_timeout(500)
            _wait_no_loading(page)

    # Save the form to apply changes before confirming
    from benchmark.oracle_helpers import save_form
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
