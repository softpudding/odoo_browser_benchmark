"""Oracle for stock.update_product_internal_reference.

Open product Steel Bracket 12 from the Products list, change the Internal
Reference to SB-12-BENCH, and click Save.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    ensure_list_view,
    fill_field,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    save_form,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-stock.product_template_action_product")
    _wait_no_loading(page)
    ensure_list_view(page)

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
