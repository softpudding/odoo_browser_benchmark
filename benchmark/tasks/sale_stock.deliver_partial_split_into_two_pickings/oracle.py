"""Oracle for sale_stock.deliver_partial_split_into_two_pickings.

Confirm multi-line SO 'S-BENCH-SPLIT-001', open delivery, set Alpha Done=5
and Beta Done=3 (forcing a partial split), validate, create backorder.
Then open the backorder picking and edit Beta Done from the auto-reserved
5 down to 0 and SAVE (no validate).
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
    save_form,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def _maybe_dismiss_warning(page):
    """Dismiss any modal that may pop up after Confirm (insufficient stock)."""
    page.wait_for_timeout(800)
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        for label in (
            "Confirm", "Continue", "Yes", "Ok", "OK", "Validate", "Proceed",
        ):
            btn = modal.last.locator(f"button:has-text('{label}')")
            if btn.count() > 0:
                btn.first.click()
                page.wait_for_timeout(800)
                _wait_no_loading(page)
                return
        primary = modal.last.locator("button.btn-primary")
        if primary.count() > 0:
            primary.first.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)


def _row_index_for_product(page, product_text):
    """Return the 0-indexed position of the o2m row that contains
    ``product_text`` in its textual content."""
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    n = rows.count()
    for i in range(n):
        if product_text in rows.nth(i).inner_text():
            return i
    return None


def _set_qty_for_product(page, product_text, value):
    """Robustly set the 'quantity' (Done) cell for the row matching
    ``product_text``. Handles the case where the cell needs an explicit
    triple-click to clear and a Tab press to commit."""
    idx = _row_index_for_product(page, product_text)
    if idx is None:
        idx = 0  # fallback

    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row"
    ).nth(idx)
    cell = row.locator(
        "td[name='quantity'], .o_field_widget[name='quantity']"
    ).first
    cell.click()
    page.wait_for_timeout(300)

    inp = cell.locator("input").first
    # Clear robustly: select all + delete + fill
    inp.click(click_count=3)
    page.wait_for_timeout(100)
    inp.fill("")
    inp.fill(str(value))
    inp.press("Tab")
    page.wait_for_timeout(600)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    clear_search_filters(page)
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    ensure_list_view(page)
    page.wait_for_timeout(500)

    # Open the target quotation by client_order_ref.
    click_list_row(page, "S-BENCH-SPLIT-001")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Confirm
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _maybe_dismiss_warning(page)

    # Open delivery
    click_stat_button(page, "Delivery")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Manually edit Done qtys: Alpha=5 (already), Beta=3 (force partial)
    _set_qty_for_product(page, "Alpha", "5")
    _set_qty_for_product(page, "Beta", "3")

    # Validate the partial delivery
    click_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Backorder dialog -> Create Backorder
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Create Backorder')"
        ).first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)

    # Navigate to the backorder picking. After validating, we're on the
    # original (now Done) picking. Go back to the SO via breadcrumb.
    page.wait_for_timeout(800)
    breadcrumbs = page.locator(".o_breadcrumb .breadcrumb-item a")
    if breadcrumbs.count() > 0:
        breadcrumbs.last.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
        page.wait_for_timeout(800)

    # Click Delivery smart button — opens a list with 2 pickings.
    click_stat_button(page, "Delivery")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Find the backorder row (not 'Done').
    list_rows = page.locator(".o_list_view .o_data_row")
    if list_rows.count() > 1:
        clicked = False
        n_rows = list_rows.count()
        for i in range(n_rows):
            txt = list_rows.nth(i).inner_text()
            # Done state badge appears as just "Done" alone; backorder shows
            # Ready / Waiting / Available / Assigned. Avoid rows with "Done".
            if "Done" not in txt:
                # Click the row's name cell so we navigate to the form.
                name_cell = list_rows.nth(i).locator("td[name='name']").first
                if name_cell.count() > 0:
                    name_cell.click(force=True)
                else:
                    list_rows.nth(i).click(force=True)
                page.wait_for_load_state("load")
                _wait_for_ready(page)
                clicked = True
                break
        if not clicked:
            list_rows.last.click(force=True)
            page.wait_for_load_state("load")
            _wait_for_ready(page)

    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # On the backorder picking: edit Beta Done from 5 -> 0.
    _set_qty_for_product(page, "Beta", "0")
    page.wait_for_timeout(500)

    # Save the form (no validate). The save_form helper clicks the cloud icon.
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Defensive second save in case the first didn't catch.
    page.wait_for_timeout(500)
    sb = page.locator(
        ".o_form_button_save:visible, button.o_form_button_save:visible"
    )
    if sb.count() > 0:
        try:
            sb.first.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)
        except Exception:
            pass


run_oracle(oracle)
