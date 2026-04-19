"""Oracle for sale_purchase.mto_so_generate_po_change_vendor_confirm.

Workflow:
  Sales -> open draft quotation S-BENCH-MTO-001 -> Confirm SO ->
  Purchase smart button -> change vendor from Alpha Precision Parts to
  Orion Component Works -> Confirm Order on the PO.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_status_button,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    save_form,
    search_for,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


SO_REF = "S-BENCH-MTO-001"
VENDOR_ALT = "Orion Component Works"


def _open_so(page):
    # Sales menu defaults to Quotations (My Quotations filter).
    # Clear filters, search by customer reference, open.
    clear_search_filters(page)
    _wait_no_loading(page)
    page.wait_for_timeout(500)
    ensure_list_view(page)
    page.wait_for_timeout(500)

    search_for(page, SO_REF)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    row = page.locator(".o_list_view .o_data_row").first
    row.wait_for(state="visible", timeout=15000)
    cells = row.locator("td")
    target = cells.nth(2) if cells.count() > 2 else cells.first
    target.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    _open_so(page)

    # --- 1. Confirm the SO ---
    click_status_button(page, "Confirm")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # --- 2. Click the Purchase smart button on the confirmed SO ---
    smart = page.locator(
        "button[name='action_view_purchase_orders']:visible"
    ).first
    smart.wait_for(state="visible", timeout=15000)
    smart.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # MTO generates a single PO per vendor, so the smart button usually
    # opens the RFQ form directly. If it shows a list, click the first row.
    if (page.locator(".o_list_view .o_data_row").count() > 0
            and page.locator(".o_form_view").count() == 0):
        page.locator(".o_list_view .o_data_row").first.locator("td").first.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
        page.wait_for_timeout(800)

    # --- 3. Swap vendor ---
    set_many2one(page, "partner_id", VENDOR_ALT)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Persist the vendor change before confirming; some Odoo 19 button
    # handlers don't auto-save the dirty partner field first.
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # --- 4. Confirm the RFQ into a PO ---
    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    _wait_for_ready(page)


run_oracle(oracle)
