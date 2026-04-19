"""Oracle for sale.configure_pricelist_apply_to_order_line.

Two-stage workflow:
 1. Sales > Products > Pricelists > New
    - Name: "Bench 10% Off"
    - Add a pricelist rule (modal form pops up):
        * Keep Apply To = Product (default), leave the product field empty
          so applied_on resolves to '3_global' (All Products).
        * Set Price Type = Formula.
        * In the formula sub-section: base = Sales Price (default),
          Discount = 10.
        * Save & Close the rule dialog.
    - Save the pricelist.
 2. Sales > Orders > Quotations > New
    - Customer: "Bench Price Co"
    - Pricelist: "Bench 10% Off"
    - Add a line: Bench Price Item, qty 1 -> price_unit auto-computes to 180.
    - Save (do NOT confirm).
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    fill_field,
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

    # ---------- Stage 1: Create the pricelist ----------
    navigate(page, "/odoo/pricelists")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    click_create(page)
    page.wait_for_timeout(800)

    # Pricelist name (H1 header)
    fill_field(page, "name", "Bench 10% Off")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Click "Add a line" in the Sales Prices tab (item_ids o2m).
    # This opens a pricelist-rule form dialog (modal).
    click_add_a_line(page)
    page.wait_for_timeout(800)

    # Wait for the pricelist-rule modal
    page.wait_for_selector(".modal:visible", timeout=10000)
    modal = page.locator(".modal:visible").last

    # Price Type radio: pick "Formula"
    # The compute_price field is a radio widget. Click the "Formula" radio.
    formula_radio = modal.locator(
        ".o_field_widget[name='compute_price'] label:has-text('Formula'), "
        ".o_field_widget[name='compute_price'] input[data-value='formula']"
    )
    formula_radio.first.click()
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    # Set Discount (price_discount) = 10
    # The formula sub-section (pricelist_rule_base) becomes visible once
    # compute_price == 'formula'. The price_discount field is a plain Float.
    discount_widget = modal.locator(".o_field_widget[name='price_discount']").first
    discount_input = discount_widget.locator("input")
    discount_input.first.click()
    discount_input.first.fill("")
    discount_input.first.fill("10")
    discount_input.first.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Click Save & Close in the modal footer
    modal = page.locator(".modal:visible").last
    save_close = modal.locator(
        ".modal-footer button.o_form_button_save, "
        ".modal-footer button:has-text('Save & Close'), "
        ".modal-footer button:has-text('Save')"
    )
    save_close.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Save the pricelist itself
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # ---------- Stage 2: Create the Sales Order ----------
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    click_create(page)
    page.wait_for_timeout(800)

    # Customer
    set_many2one(page, "partner_id", "Bench Price Co")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Pricelist on SO header
    set_many2one(page, "pricelist_id", "Bench 10% Off")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Add order line (Bench Price Item, qty 1)
    click_add_a_line(page)
    page.wait_for_timeout(600)

    # SO lines list exposes product_template_id in the column, not product_id
    set_o2m_many2one(page, 0, "product_template_id", "Bench Price Item")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # qty is 1 by default; set explicitly to be safe
    set_o2m_field(page, 0, "product_uom_qty", "1")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Save (do NOT confirm)
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
