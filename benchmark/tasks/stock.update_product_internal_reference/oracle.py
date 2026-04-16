"""Oracle for stock.update_product_internal_reference.

Open product Steel Bracket 12 from the Products list, change the Internal
Reference to SB-12-BENCH, and click Save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    fill_field,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)

    # Navigate to Products list
    page.click('a:has-text("Products")')
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Find and open the product
    click_list_row(page, "Steel Bracket 12")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Change the Internal Reference
    fill_field(page, "default_code", "SB-12-BENCH")

    # Click Save
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
