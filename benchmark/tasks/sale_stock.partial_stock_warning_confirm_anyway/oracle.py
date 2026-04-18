"""Oracle for sale_stock.partial_stock_warning_confirm_anyway.

Confirm draft SO 'S-BENCH-STK-001' (dismiss any insufficient-stock warning),
navigate to its delivery via the smart button, ensure Done qty = 2 on the
single move, click Validate, and pick 'Create Backorder' in the wizard.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_button,
    click_list_row,
    click_stat_button,
    click_status_button,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def _maybe_dismiss_warning(page):
    """Dismiss any modal that may appear after Confirm.

    Odoo 19 may pop a 'Not enough inventory' or insufficient-stock dialog;
    we click any primary 'Confirm'/'Ok'/'Yes'/'Continue' button. If no modal
    appears, this is a no-op.
    """
    page.wait_for_timeout(800)
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        # Try the typical override buttons in priority order.
        for label in (
            "Confirm",
            "Continue",
            "Yes",
            "Ok",
            "OK",
            "Validate",
            "Proceed",
        ):
            btn = modal.last.locator(f"button:has-text('{label}')")
            if btn.count() > 0:
                btn.first.click()
                page.wait_for_timeout(800)
                _wait_no_loading(page)
                return
        # Last resort: click the first primary button.
        primary = modal.last.locator("button.btn-primary")
        if primary.count() > 0:
            primary.first.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Remove default "My Quotations" filter so we can see all quotations.
    clear_search_filters(page)
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    ensure_list_view(page)
    page.wait_for_timeout(500)

    # Click the Bench Warehouse Co row (the SO is S-BENCH-STK-001).
    click_list_row(page, "S-BENCH-STK-001")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Confirm the quotation.
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Dismiss any warning dialog (insufficient stock, etc.).
    _maybe_dismiss_warning(page)

    # Click the Delivery smart button.
    click_stat_button(page, "Delivery")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Done qty should already be 2 (the available reservation).
    # Set it explicitly to be safe.
    try:
        set_o2m_field(page, 0, "quantity", "2")
        page.wait_for_timeout(500)
    except Exception:
        pass

    # Validate the delivery.
    click_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Backorder dialog -> click Create Backorder.
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Create Backorder')"
        ).first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
