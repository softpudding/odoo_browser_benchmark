"""Oracle for website_sale.publish_product_shop.

UI flow (same as a browser agent):
  1. Log into Odoo.
  2. Navigate to the eCommerce Products list (/odoo/ecommerce-products).
  3. Open the seeded 'Bench Gadget Pro' product form.
  4. Set the Sales Price (list_price) to 99.00.
  5. Open the Sales tab and toggle the is_published switch on.
  6. Save the form.
"""

from benchmark.oracle_helpers import (
    _wait_no_loading,
    click_list_row,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/ecommerce-products")
    _wait_no_loading(page)

    click_list_row(page, "Bench Gadget Pro")
    _wait_no_loading(page)

    # Update the Sales Price (list_price) shown in the General Information tab.
    fill_field(page, "list_price", "99.00")

    # The is_published boolean_toggle lives in the Sales tab's eCommerce Shop
    # group on the product form. Open the tab before locating it.
    try:
        click_tab(page, "Sales")
    except Exception:
        pass
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    publish_toggle = page.locator(
        ".o_field_widget[name='is_published'] input[type='checkbox']"
    ).last
    publish_toggle.wait_for(state="attached", timeout=10000)
    if not publish_toggle.is_checked():
        publish_toggle.click(force=True)
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
