"""Oracle for sale_purchase.mto_so_generate_po_change_vendor_confirm.

Walks through the MTO SO->PO smart-button chain:
    1. Open the sales order S-BENCH-MTO-001.
    2. Click the Purchase smart-button to jump to the auto-generated draft
       RFQ for Acme Supply Co.
    3. Replace the vendor on the RFQ with Brook Trading Ltd; save so the
       line price_unit recomputes to 40.00.
    4. Click Confirm Order so the PO state becomes 'purchase'.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


SO_NAME = "S-BENCH-MTO-001"
VENDOR_B = "Brook Trading Ltd"


def _click_purchase_smart_button(page):
    # The smart button renders as ".oe_stat_button" with an inner span
    # labelled "Purchase".
    btn = page.locator(
        ".oe_stat_button:has(span:has-text('Purchase'))"
    ).first
    if btn.count() == 0:
        # Fall back to a named action ref
        btn = page.locator(
            "button[name='action_view_purchase_orders']:visible"
        ).first
    btn.wait_for(state="visible", timeout=15000)
    btn.scroll_into_view_if_needed()
    btn.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def _change_po_vendor(page, vendor_name):
    # The vendor input on a purchase.order form is [name='partner_id'].
    field = page.locator(
        ".o_form_view .o_field_widget[name='partner_id']"
    ).first
    field.wait_for(state="visible", timeout=15000)
    field.scroll_into_view_if_needed()
    inp = field.locator("input").first
    inp.click()
    # Select-all then type replacement.
    inp.press("Control+a")
    inp.press("Delete")
    inp.fill(vendor_name)
    page.wait_for_timeout(700)
    # Pick from the dropdown (could be ".dropdown-menu" or ".ui-autocomplete")
    option = page.locator(
        ".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item"
    ).filter(has_text=vendor_name).first
    option.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)


def _save_form(page):
    # Cloud-save button in the cog/breadcrumb area.
    save_btn = page.locator(
        ".o_form_button_save:visible, "
        ".o_control_panel button:has-text('Save'):visible, "
        "button.o_form_button_save:visible"
    ).first
    if save_btn.count() > 0:
        try:
            save_btn.click()
        except Exception:
            pass
    page.wait_for_timeout(800)
    _wait_no_loading(page)


def _confirm_po(page):
    btn = page.locator(
        ".o_statusbar_buttons button[name='button_confirm']:visible, "
        "button[name='button_confirm']:visible"
    ).first
    btn.wait_for(state="visible", timeout=15000)
    btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    # No warning modal expected here (the PO has no alternatives), but
    # defend in case one appears.
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        primary = modal.last.locator(
            "button.btn-primary:visible, "
            "button:has-text('Ok'):visible, "
            "button:has-text('Confirm'):visible"
        )
        if primary.count() > 0:
            try:
                primary.first.click()
            except Exception:
                pass
            page.wait_for_timeout(1000)
            _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # --- 1. Open the SO ---
    click_list_row(page, SO_NAME)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # --- 2. Jump to the MTO-generated RFQ ---
    _click_purchase_smart_button(page)

    # If the smart-button lands on a list (multiple POs), click the only row.
    list_rows = page.locator(".o_list_renderer .o_data_row")
    if list_rows.count() >= 1 and page.locator(".o_form_view").count() == 0:
        list_rows.first.click()
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    # --- 3. Switch vendor to Brook Trading Ltd + save ---
    _change_po_vendor(page, VENDOR_B)
    _save_form(page)

    # --- 4. Confirm the PO ---
    _confirm_po(page)


run_oracle(oracle)
