"""Oracle for product.set_product_category_change.

Open Inventory > Products, open the seeded 'Bench Cat Item', change the
Product Category m2o from 'All' to 'Office Supplies' via autocomplete,
and save.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


PRODUCT_NAME = "Bench Cat Item"
CATEGORY_NAME = "Office Supplies"


def oracle(page):
    login(page)

    # Navigate directly to the product list.
    navigate(page, "/odoo/action-stock.product_template_action_product")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    ensure_list_view(page)
    page.wait_for_timeout(400)

    # Open the seeded product.
    click_list_row(page, PRODUCT_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(600)

    # Change the Product Category many2one to Office Supplies.
    set_many2one(page, "categ_id", CATEGORY_NAME)
    page.wait_for_timeout(400)

    # Save the form.
    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)


run_oracle(oracle)
