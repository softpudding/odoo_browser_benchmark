"""Oracle for mrp.create_routing_set_workcenter.

1. Go to Work Centers list, create a new workcenter named
   'Benchmark Assembly Station'.
2. Go to the BOM list, open BOM for 'Benchmark Frame Assembly'.
3. Click the Operations tab. Because the BOM has 0 ops, the tab shows an
   'Add Operation' button that calls `mrp.bom.action_open_operation_form`.
   That action opens a full-page routing.workcenter form with default_bom_id
   already set. Fill Name='Final Assembly', Work Center=new workcenter, and
   Expected Duration=30 minutes, save.
"""

from benchmark.oracle_helpers import (
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


WORKCENTER_NAME = "Benchmark Assembly Station"
PRODUCT_NAME = "Benchmark Frame Assembly"


def oracle(page):
    login(page)

    # ---- Step 1: create the new work center --------------------------------
    navigate(page, "/odoo/workcenters")
    _wait_no_loading(page)
    page.wait_for_timeout(800)
    click_create(page)
    _wait_for_ready(page)

    fill_field(page, "name", WORKCENTER_NAME)
    save_form(page)
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # ---- Step 2: open the seeded BOM ---------------------------------------
    navigate(page, "/odoo/boms")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    row = page.locator(
        f".o_data_row:has-text('{PRODUCT_NAME}')"
    ).first
    row.click()
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # ---- Step 3: click the Operations tab ----------------------------------
    page.locator("a.nav-link:has-text('Operations')").first.click()
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    # Since the BOM has no operations, the x2many list is hidden and instead
    # an "Add Operation" button is shown. Clicking it calls
    # mrp.bom.action_open_operation_form which opens a full-page form for the
    # new routing.workcenter with default_bom_id set.
    add_op_btn = page.locator(
        "button[name='action_open_operation_form']:visible, "
        "button:has-text('Add Operation'):visible"
    )
    add_op_btn.first.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # We should now be on a fresh mrp.routing.workcenter form. Fill fields.
    # The operation name field renders as a <text> widget in an <h1>, so use
    # textarea selector.
    name_widget = page.locator(
        ".o_field_widget[name='name']"
    ).first
    # Try textarea first (the form uses widget='text' for name)
    name_inp = name_widget.locator("textarea, input").first
    name_inp.click()
    name_inp.fill("")
    name_inp.fill("Final Assembly")
    name_inp.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    set_many2one(page, "workcenter_id", WORKCENTER_NAME)
    page.wait_for_timeout(400)

    fill_field(page, "time_cycle_manual", "30")
    page.wait_for_timeout(400)

    save_form(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)


run_oracle(oracle)
