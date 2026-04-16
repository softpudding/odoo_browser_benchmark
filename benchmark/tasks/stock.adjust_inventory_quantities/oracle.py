"""Oracle for stock.adjust_inventory_quantities.

Navigate to Inventory > Operations > Physical Inventory.
Edit on-hand quantities for 3 specific products (Steel Bracket 12", Copper Wire 100m,
Safety Harness XL) to their target values, leaving 2 distractor products unchanged.
Click Apply All.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


ADJUSTMENTS = [
    ('Steel Bracket 12"', "45"),
    ("Copper Wire 100m", "120"),
    ("Safety Harness XL", "8"),
]


def _search_product(page, product_name: str) -> None:
    """Clear search and search for a specific product in Physical Inventory."""
    for _ in range(5):
        close_btn = page.locator(".o_facet_remove").first
        if close_btn.count() == 0 or not close_btn.is_visible():
            break
        close_btn.click()
        page.wait_for_timeout(200)
    search_inp = page.locator(".o_searchview_input").first
    search_inp.click()
    search_inp.fill(product_name[:15])  # partial name avoids CSS quote issues
    page.wait_for_timeout(400)
    search_inp.press("Enter")
    page.wait_for_timeout(600)
    _wait_no_loading(page)


def _clear_search(page) -> None:
    for _ in range(5):
        close_btn = page.locator(".o_facet_remove").first
        if close_btn.count() == 0 or not close_btn.is_visible():
            break
        close_btn.click()
        page.wait_for_timeout(200)
    _wait_no_loading(page)


def _set_inventory_qty(page, product_name: str, qty: str) -> None:
    """Find a row in Physical Inventory by product name and set its quantity."""
    _search_product(page, product_name)

    # Use .filter() to avoid CSS quoting issues with special chars (e.g. " in product names)
    row = page.locator(".o_data_row").filter(has_text=product_name).first
    row.wait_for(state="visible", timeout=8000)

    qty_cell = row.locator("[name='inventory_quantity']").first
    qty_cell.click()
    page.wait_for_timeout(400)

    active_input = row.locator("[name='inventory_quantity'] input")
    if active_input.count() > 0 and active_input.first.is_visible():
        active_input.first.click(click_count=3)
        active_input.first.fill(qty)
        active_input.first.press("Tab")
    else:
        qty_cell.dblclick()
        page.wait_for_timeout(400)
        active_input = row.locator("[name='inventory_quantity'] input")
        if active_input.count() > 0:
            active_input.first.fill(qty)
            active_input.first.press("Tab")

    page.wait_for_timeout(400)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)

    # Navigate to Operations > Physical Inventory
    page.locator("a.nav-link:has-text('Operations'), span:has-text('Operations')").first.click()
    page.wait_for_timeout(500)
    page.locator(
        ".o_menu_sections a:has-text('Physical Inventory'), "
        ".dropdown-menu a:has-text('Physical Inventory')"
    ).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Set quantities for each target product
    for product_name, qty in ADJUSTMENTS:
        _set_inventory_qty(page, product_name, qty)

    # Clear search filters before clicking Apply All (ensures all adjusted quants are included)
    _clear_search(page)
    page.wait_for_timeout(500)

    # Click Apply All — opens the "Inventory Adjustment" wizard dialog
    apply_btn = page.locator("button[name='action_apply_all']:visible").first
    apply_btn.wait_for(state="visible", timeout=5000)
    apply_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # The wizard asks for a reason — click "Update Quantities" to confirm
    dialog_btn = page.locator(
        ".modal:visible button[name='action_apply']:visible, "
        ".o_dialog:visible button[name='action_apply']:visible, "
        ".modal:visible button:has-text('Update Quantities'):visible, "
        ".o_dialog:visible button:has-text('Update Quantities'):visible"
    )
    if dialog_btn.count() > 0:
        dialog_btn.first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)
    else:
        # Fallback: any primary button in any visible dialog
        fallback = page.locator(".modal:visible button.btn-primary, .o_dialog:visible button.btn-primary")
        if fallback.count() > 0:
            fallback.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)


run_oracle(oracle)
