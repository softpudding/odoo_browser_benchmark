"""Oracle for stock.confirm_and_validate_receipt.

Find receipt BENCH-RCV-01 in transfers, set done quantities for each line
to match demand, and validate.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    clear_search_filters,
    ensure_list_view,
    login,
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

    # Navigate to Operations > Transfers
    # Try the menu path or direct URL
    navigate(page, "/odoo/inventory/picking-type-all")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # If that didn't work, try through the menu
    rows = page.locator(".o_list_view .o_data_row, .o_kanban_view .o_kanban_record")
    if rows.count() == 0:
        navigate(page, "/odoo/inventory")
        _wait_no_loading(page)
        # Try clicking Operations > Transfers in the menu
        menu = page.locator("button.dropdown-toggle:has-text('Operations'):visible")
        if menu.count() > 0:
            menu.first.click()
            page.wait_for_timeout(500)
            page.locator(".dropdown-menu:visible .dropdown-item:has-text('Transfers')").first.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)

    # Find the receipt by its origin reference
    clear_search_filters(page)
    ensure_list_view(page)
    click_list_row(page, "BENCH-RCV-01")
    page.wait_for_timeout(500)

    # Set done quantities for each move line
    # Steel Bracket 12" -> 20, Copper Wire 100m -> 10
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    for i in range(rows.count()):
        row_text = rows.nth(i).inner_text()
        if "Steel Bracket" in row_text:
            set_o2m_field(page, i, "quantity", "20")
            page.wait_for_timeout(300)
        elif "Copper Wire" in row_text:
            set_o2m_field(page, i, "quantity", "10")
            page.wait_for_timeout(300)

    page.wait_for_timeout(500)

    # Click Validate
    click_status_button(page, "Validate")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # If a confirmation dialog appears (immediate transfer), click Apply/OK
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        apply_btn = modal.last.locator(
            "button:has-text('Apply'), button:has-text('Ok'), "
            "button.btn-primary"
        )
        if apply_btn.count() > 0:
            apply_btn.first.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)


run_oracle(oracle)
