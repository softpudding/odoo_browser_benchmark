"""Oracle for sale_stock.confirm_so_manual_reserve_validate_delivery.

Confirm the draft quotation for Bench SO Customer, navigate to the
outgoing delivery via the smart button, click Check Availability to
manually reserve stock, and validate the delivery so all 5 units are
delivered in a single shipment.
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
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Drop the default "My Quotations" filter so all quotations are visible
    clear_search_filters(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    ensure_list_view(page)
    page.wait_for_timeout(500)

    # Open the draft quotation for Bench SO Customer
    row = page.locator(
        ".o_list_view .o_data_row:has-text('Bench SO Customer')"
    ).first
    cell = row.locator(
        "td[name='partner_id'], td:has-text('Bench SO Customer')"
    ).first
    cell.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Confirm the quotation
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Dismiss any post-confirmation dialog
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Ok'), button.btn-primary"
        ).first.click()
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    # Click the Delivery smart button to open the stock.picking
    click_stat_button(page, "Delivery")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Some deliveries arrive on a list view if there are multiple — pick one
    if page.locator(".o_list_view .o_data_row").count() > 0 and \
            page.locator(".o_form_view").count() == 0:
        page.locator(".o_list_view .o_data_row").first.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    # Click "Check Availability" to manually reserve stock.
    # In Odoo 19 this button is labelled "Check Availability" and has
    # name='action_assign'.
    check_btn = page.locator(
        "button[name='action_assign']:visible"
    ).first
    if check_btn.count() > 0:
        check_btn.click()
        page.wait_for_load_state("load")
        page.wait_for_timeout(1000)
        _wait_no_loading(page)
    else:
        # Fallback: click by label text
        try:
            click_button(page, "Check Availability")
        except Exception:
            pass
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    # Validate the delivery
    validate_btn = page.locator(
        "button[name='button_validate']:visible"
    ).first
    if validate_btn.count() > 0:
        validate_btn.click()
    else:
        click_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # If an unexpected backorder / transfer dialog appears, dismiss it by
    # picking "No Backorder" so we fully validate the 5 units.
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        no_bo = modal.last.locator("button:has-text('No Backorder')")
        if no_bo.count() > 0:
            no_bo.first.click()
        else:
            # Generic primary confirmation (immediate transfer, etc.)
            modal.last.locator(
                "button.btn-primary, button:has-text('Apply'), "
                "button:has-text('Ok')"
            ).first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
