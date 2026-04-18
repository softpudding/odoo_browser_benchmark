"""Oracle for sale_purchase.update_pol_alternative_vendor_compare.

Walks through the alternative-RFQ workflow end-to-end:
    1. Open Atlas Industrial RFQ R-BENCH-ALT-001.
    2. Use the Alternatives tab → Create Alternative wizard to add
       Beacon Mechanical, set its line price to 100.
    3. Navigate back, add Crestline Equipment, set its line price to 130.
    4. Cancel the Atlas and Crestline RFQs (the prompt allows this branch
       to be reached either via the Compare-Product-Lines "Choose" button
       or by directly cancelling losing alternatives — both leave the same
       final state).
    5. Confirm Beacon Mechanical's RFQ.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


VENDOR_A = "Atlas Industrial"
VENDOR_B = "Beacon Mechanical"
VENDOR_C = "Crestline Equipment"
RFQ_REF = "R-BENCH-ALT-001"


def _open_alternatives_tab(page):
    tab = page.locator(
        ".o_notebook .nav-link:has-text('Alternatives'):visible"
    ).first
    tab.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _add_alternative(page, vendor_name):
    _open_alternatives_tab(page)
    btn = page.locator(
        "button[name='action_create_alternative']:visible"
    ).first
    btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last
    modal.wait_for(state="visible")
    inp = modal.locator(
        ".o_field_widget[name='partner_ids'] input"
    ).first
    inp.click()
    inp.fill(vendor_name)
    page.wait_for_timeout(800)
    item = page.locator(
        ".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item"
    ).filter(has_text=vendor_name).first
    item.click()
    page.wait_for_timeout(500)

    create_btn = modal.locator(
        "button[name='action_create_alternative']:visible, "
        "button:has-text('Create Alternative'):visible"
    ).first
    create_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def _set_first_line_price(page, price):
    products_tab = page.locator(
        ".o_notebook .nav-link:has-text('Products'):visible"
    )
    if products_tab.count() > 0:
        products_tab.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row"
    ).first
    row.wait_for(state="visible", timeout=15000)
    row.scroll_into_view_if_needed()
    cell = row.locator("td[name='price_unit']").first
    cell.click()
    page.wait_for_timeout(400)
    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(str(price))
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)
    save = page.locator(
        ".o_form_button_save:visible, .o_control_panel button:has-text('Save'):visible"
    )
    if save.count() > 0:
        save.first.click()
        page.wait_for_timeout(800)
    _wait_no_loading(page)


def _cancel_current_po(page):
    """Click the Cancel button on the current PO form."""
    btn = page.locator(
        "button[name='button_cancel']:visible"
    ).first
    btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    # Confirm any modal
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        ok = modal.last.locator(
            "button:has-text('Ok'):visible, button:has-text('Confirm'):visible, "
            "button.btn-primary:visible"
        )
        if ok.count() > 0:
            ok.first.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)


def _open_po_by_partner(page, vendor_name):
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)
    click_list_row(page, vendor_name)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    # --- 1. Open Atlas Industrial RFQ ---
    click_list_row(page, RFQ_REF)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # --- 2. Add Beacon Mechanical alternative + price 100 ---
    _add_alternative(page, VENDOR_B)
    _set_first_line_price(page, 100)

    # --- 3. Go back to Atlas via the purchase list and add Crestline + 130 ---
    _open_po_by_partner(page, VENDOR_A)
    _add_alternative(page, VENDOR_C)
    _set_first_line_price(page, 130)

    # --- 4. Cancel Atlas, then Crestline ---
    _open_po_by_partner(page, VENDOR_A)
    _cancel_current_po(page)

    _open_po_by_partner(page, VENDOR_C)
    _cancel_current_po(page)

    # --- 5. Confirm Beacon Mechanical ---
    _open_po_by_partner(page, VENDOR_B)
    confirm = page.locator(
        ".o_statusbar_buttons button[name='button_confirm']:visible"
    ).first
    confirm.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    # No alternatives remaining → no warning dialog expected, but handle it
    # defensively in case Odoo still shows one.
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        cancel_alts = modal.last.locator(
            "button[name='action_cancel_alternatives']:visible, "
            "button:has-text('Cancel Alternatives'):visible, "
            "button:has-text('Ok'):visible, "
            "button.btn-primary:visible"
        )
        if cancel_alts.count() > 0:
            cancel_alts.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)


run_oracle(oracle)
