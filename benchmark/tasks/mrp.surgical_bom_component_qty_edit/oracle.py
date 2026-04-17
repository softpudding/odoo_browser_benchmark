"""Oracle for mrp.surgical_bom_component_qty_edit.

Open the BOM for Benchmark Assembly Gamma, change Gamma Bolt M6 qty
from 4 to 6, save.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-mrp.mrp_bom_form_action")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Clear filters.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break

    click_list_row(page, "Benchmark Assembly Gamma")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Find the Gamma Bolt M6 row. Click its qty cell to enter edit mode
    # then fill via the input that appears.
    row = page.locator(
        "tr.o_data_row:has-text('Gamma Bolt M6')"
    ).first
    row.wait_for(state="visible", timeout=15000)
    qty_cell = row.locator("td[name='product_qty']").first
    qty_cell.click()
    page.wait_for_timeout(300)
    # Try to locate the input that becomes active.
    qty_input = page.locator(
        "tr.o_data_row:has-text('Gamma Bolt M6') td[name='product_qty'] input, "
        "tr.o_data_row.o_selected_row td[name='product_qty'] input"
    ).first
    try:
        qty_input.wait_for(state="visible", timeout=5000)
        qty_input.fill("6")
        page.keyboard.press("Tab")
    except Exception:
        # Fallback: dblclick, then use keyboard.
        qty_cell.dblclick()
        page.wait_for_timeout(300)
        page.keyboard.press("Meta+a")
        page.keyboard.type("6")
        page.keyboard.press("Tab")
    page.wait_for_timeout(600)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
