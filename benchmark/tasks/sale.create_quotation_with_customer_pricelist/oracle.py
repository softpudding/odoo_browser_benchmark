"""Oracle for sale.create_quotation_with_customer_pricelist.

Create a draft quotation for 'Bench Premium Co' (has 'VIP 20% Off'
pricelist). Add 5x 'Bench Standard Widget'. Save (do NOT confirm) —
pricelist auto-applies a 20% discount → unit price 80.00.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # New quotation
    click_create(page)
    page.wait_for_timeout(500)

    # Set customer — triggers pricelist auto-apply
    set_many2one(page, "partner_id", "Bench Premium Co")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Add the single order line: Bench Standard Widget, qty 5
    click_add_a_line(page)
    page.wait_for_timeout(600)

    # sol_o2m list view exposes product_template_id, not product_id
    set_o2m_many2one(page, 0, "product_template_id", "Bench Standard Widget")
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    set_o2m_field(page, 0, "product_uom_qty", "5")
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    # Save (do not confirm). Press Escape first to close any open m2o popover.
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
