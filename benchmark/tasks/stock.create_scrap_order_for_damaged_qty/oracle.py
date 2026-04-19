"""Oracle for stock.create_scrap_order_for_damaged_qty.

Flow:
  1. Navigate to Inventory > Operations > Scrap (action_stock_scrap).
  2. Click New to open the scrap form.
  3. Set Product = 'Bench Scrap Item' (product m2o).
  4. Set Quantity = 3 (overwrite default 1.0).
  5. Save the form.
  6. Click Validate on the header to push state 'draft' -> 'done'.

UI has several quirks we accept:
  * action_stock_scrap opens as a list view with header 'Scrap Orders'
    and a 'New' button; the form view has 'scrap_qty' field labelled
    Quantity, 'product_id' many2one, 'location_id' / 'scrap_location_id'
    many2one fields (shown only with stock.group_stock_multi_locations,
    which seed grants).
  * The Validate button is in the form statusbar
    (`button_box`/`header`) and wires to
    `stock.scrap.action_validate`.
  * On Validate Odoo does NOT pop a wizard when the source has enough
    stock (seed gives 10 >= 3). The button toggles state -> done.
"""

from benchmark.oracle_helpers import (
    click_button,
    click_create,
    full_url,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)

PRODUCT_NAME = "Bench Scrap Item"


def _open_scrap_list(page):
    # Direct URL to the Scrap Orders action. The Odoo 19 action is
    # `stock.action_stock_scrap`. Use the server-action redirect
    # pattern so we land on the list view regardless of menu shape.
    page.goto(full_url("/odoo/action-stock.action_stock_scrap"), timeout=60000)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


def _fill_product(page, name):
    # Use the many2one helper targeting the product_id field.
    set_many2one(page, "product_id", name)
    page.wait_for_timeout(600)
    _wait_no_loading(page)


def _fill_quantity(page, qty):
    widget = page.locator(".o_field_widget[name='scrap_qty']").first
    widget.wait_for(state="visible", timeout=10000)
    inp = widget.locator("input").first
    inp.click()
    inp.press("Control+A")
    inp.press("Meta+A")
    inp.fill("")
    inp.type(str(qty))
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _click_validate(page):
    # The Validate button lives in the statusbar as a primary action.
    btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Validate'), "
        ".o_form_statusbar button:visible:has-text('Validate'), "
        "button[name='action_validate']:visible"
    ).first
    btn.wait_for(state="visible", timeout=15000)
    btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # If Odoo pops any downstream wizard (unexpected — we seeded enough
    # stock) just confirm it with the primary button.
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        m = modal.last
        pbtn = m.locator("button.btn-primary:visible").first
        if pbtn.count() > 0:
            pbtn.click()
            page.wait_for_timeout(1200)
            _wait_no_loading(page)


def oracle(page):
    login(page)

    _open_scrap_list(page)

    # New scrap order.
    click_create(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    _fill_product(page, PRODUCT_NAME)
    _fill_quantity(page, 3)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    _click_validate(page)


run_oracle(oracle)
