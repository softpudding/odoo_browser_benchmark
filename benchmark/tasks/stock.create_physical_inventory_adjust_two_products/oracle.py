"""Oracle for stock.create_physical_inventory_adjust_two_products.

Navigate to Inventory > Operations > Physical Inventory. Edit Counted
Quantity inline for Bench Prod X (15 -> 12) and Bench Prod Y (25 -> 27),
then click Apply All. Confirm the follow-up "Inventory Adjustment
Reference" / "Update Quantities" dialog.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


ADJUSTMENTS = [
    ("Bench Prod X", "12"),
    ("Bench Prod Y", "27"),
]


def _clear_search(page) -> None:
    for _ in range(6):
        close_btn = page.locator(".o_facet_remove").first
        if close_btn.count() == 0 or not close_btn.is_visible():
            break
        close_btn.click()
        page.wait_for_timeout(200)
    _wait_no_loading(page)


def _search_product(page, product_name: str) -> None:
    _clear_search(page)
    search_inp = page.locator(".o_searchview_input").first
    search_inp.click()
    search_inp.fill(product_name)
    page.wait_for_timeout(400)
    search_inp.press("Enter")
    page.wait_for_timeout(600)
    _wait_no_loading(page)


def _set_counted_qty(page, product_name: str, qty: str) -> None:
    _search_product(page, product_name)

    row = page.locator(".o_data_row").filter(has_text=product_name).first
    row.wait_for(state="visible", timeout=8000)

    # Counted Quantity binds to stock.quant.inventory_quantity in the
    # Physical Inventory list (action_view_quants, inventory_mode=True).
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
    page.locator(
        "a.nav-link:has-text('Operations'), "
        "span:has-text('Operations')"
    ).first.click()
    page.wait_for_timeout(500)
    page.locator(
        ".o_menu_sections a:has-text('Physical Inventory'), "
        ".dropdown-menu a:has-text('Physical Inventory')"
    ).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    for product_name, qty in ADJUSTMENTS:
        _set_counted_qty(page, product_name, qty)

    # Clear search so Apply All picks up both adjusted rows.
    _clear_search(page)
    page.wait_for_timeout(500)

    apply_btn = page.locator(
        "button[name='action_apply_all']:visible, "
        "button:has-text('Apply All'):visible"
    ).first
    apply_btn.wait_for(state="visible", timeout=5000)
    apply_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Confirmation dialog (Inventory Adjustment Reference / Update
    # Quantities) - click the primary action.
    dialog_btn = page.locator(
        ".modal:visible button[name='action_apply']:visible, "
        ".o_dialog:visible button[name='action_apply']:visible, "
        ".modal:visible button:has-text('Update Quantities'):visible, "
        ".o_dialog:visible button:has-text('Update Quantities'):visible, "
        ".modal:visible button:has-text('Apply'):visible, "
        ".o_dialog:visible button:has-text('Apply'):visible"
    )
    if dialog_btn.count() > 0:
        dialog_btn.first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)
    else:
        fallback = page.locator(
            ".modal:visible button.btn-primary, "
            ".o_dialog:visible button.btn-primary"
        )
        if fallback.count() > 0:
            fallback.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)


run_oracle(oracle)
