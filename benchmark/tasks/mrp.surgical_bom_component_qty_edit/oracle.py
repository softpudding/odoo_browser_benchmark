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

    # Find the Gamma Bolt M6 row in the bom_line_ids o2m and click its
    # product_qty cell to enter edit mode.
    row = page.locator(
        "tr.o_data_row:has-text('Gamma Bolt M6')"
    ).first
    row.wait_for(state="visible", timeout=15000)
    # Click the cell with field name product_qty.
    qty_cell = row.locator("td[name='product_qty']").first
    qty_cell.click()
    page.wait_for_timeout(400)
    # Now an input should be focused in that cell.
    qty_input = row.locator("td[name='product_qty'] input").first
    qty_input.fill("")
    qty_input.fill("6")
    page.keyboard.press("Tab")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
