"""Oracle for inventory.scrap_product.

Open product Steel Bracket 12", click Scrap, enter quantity 5, click Scrap button.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)

    # Find and open the product Steel Bracket 12"
    click_list_row(page, "Steel Bracket 12\"")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Click the Scrap button
    page.get_by_role("button", name="Scrap").click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Fill in the quantity field
    qty_input = page.get_by_label("Quantity")
    qty_input.fill("5")
    page.wait_for_timeout(500)

    # Click the Scrap button in the dialog
    page.get_by_role("button", name="Scrap", exact=True).last.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)