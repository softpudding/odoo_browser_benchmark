"""Oracle for sale_purchase.dropship_so_to_po_chain_validate.

Workflow:
  Sales -> open SO S-BENCH-DS-001 -> Purchase smart button ->
  Confirm Order on the draft RFQ -> Receipt smart button ->
  set Done=5 on the dropship picking -> Validate -> handle backorder dialog.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_button,
    click_stat_button,
    click_status_button,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    search_for,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    # Sales menu defaults to Quotations with "My Quotations" filter.
    # Navigate to Orders submenu so we see confirmed SOs by default.
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    orders_btn = page.locator('.o_menu_sections button:has-text("Orders")')
    if orders_btn.count() > 0:
        orders_btn.first.click()
        page.wait_for_load_state("load")
        _wait_no_loading(page)
        page.wait_for_timeout(1000)

    # Clear any default filter and search by client reference.
    clear_search_filters(page)
    _wait_no_loading(page)
    page.wait_for_timeout(500)
    ensure_list_view(page)
    page.wait_for_timeout(500)

    search_for(page, "S-BENCH-DS-001")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Open the only matching row. Click a non-checkbox cell so the row
    # opens in form view rather than just selecting it.
    row = page.locator(".o_list_view .o_data_row").first
    cells = row.locator("td")
    # td0 is usually the checkbox column — click td2/td3 (partner / date).
    target = cells.nth(2) if cells.count() > 2 else cells.first
    target.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # --- Click the Purchase smart button on the SO ---
    # The smart button has name="action_view_purchase_orders".
    page.locator(
        "button[name='action_view_purchase_orders']"
    ).first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # If the button took us to a list (only one PO usually opens directly,
    # but be defensive), open the first row.
    if page.locator(".o_list_view .o_data_row").count() > 0 and \
            page.locator(".o_form_view").count() == 0:
        page.locator(".o_list_view .o_data_row").first.locator("td").first.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
        page.wait_for_timeout(800)

    # --- Confirm the PO ---
    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # --- Click the Dropship smart button on the PO ---
    # On a dropship PO the smart button is labeled "Dropship" (not
    # "Receipt") and has name="action_view_dropship".
    page.locator(
        "button[name='action_view_dropship']"
    ).first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # If a list of pickings appears (rare for dropship), open the first row.
    if page.locator(".o_list_view .o_data_row").count() > 0 and \
            page.locator(".o_form_view").count() == 0:
        page.locator(".o_list_view .o_data_row").first.locator("td").first.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
        page.wait_for_timeout(800)

    # --- Set Done quantity = 5 on the first move row ---
    # The dropship picking pre-reserves the full demand (qty=5) so the
    # quantity is already correct, but we set it explicitly to be safe.
    try:
        set_o2m_field(page, 0, "quantity", "5")
    except Exception:
        # Field may not be editable inline if the picking auto-reserved.
        pass
    page.wait_for_timeout(500)

    # --- Validate the dropship transfer ---
    # Use the button's technical name so we don't accidentally hit a
    # different "Validate" button elsewhere on the page.
    validate_btn = page.locator("button[name='button_validate']:visible").first
    if validate_btn.count() == 0:
        # Fallback to the visible-text selector.
        click_button(page, "Validate")
    else:
        validate_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # --- Handle the optional backorder dialog: pick "No Backorder" ---
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        # Prefer "No Backorder" since the agent should ship the full qty.
        no_bo = modal.last.locator("button:has-text('No Backorder')")
        if no_bo.count() > 0:
            no_bo.first.click()
        else:
            # Fall back to any primary action / OK / Apply
            modal.last.locator(
                "button:has-text('Apply'), button:has-text('Ok'), button.btn-primary"
            ).first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
