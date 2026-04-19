"""Oracle for mrp.create_bom_kit_type_for_product.

Navigate to the Bills of Materials list, click New, pick the finished
product, flip the BoM Type radio from the default 'Manufacture this
Product' (normal) to 'Kit' (phantom), then add the two component lines
under the Components tab and save.

Calibration trap for BU: the default BoM Type radio is the 'Manufacture
this Product' option; a naive "create-from-scratch" agent leaves the
radio on the default and saves a regular (normal) BoM. The oracle must
explicitly click the 'Kit' radio.
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
    _wait_for_ready,
)


FINISHED_NAME = "Bench Kit Finished"
COMP_A_NAME = "Bench Kit Comp A"
COMP_B_NAME = "Bench Kit Comp B"


def oracle(page):
    login(page)

    navigate(page, "/odoo/action-mrp.mrp_bom_form_action")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_create(page)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # --- Select the finished product ---
    set_many2one(page, "product_tmpl_id", FINISHED_NAME)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Leave product_qty at its default (1). If the form renders it empty,
    # force it to 1 so the diff is deterministic.
    try:
        fill_field(page, "product_qty", "1")
    except Exception:
        pass

    # --- Flip BoM Type radio to Kit (phantom) ---
    # `mrp.bom.type` renders as `widget="radio"` → `div.o_field_radio`
    # with three o_radio_item children (Manufacture / Kit / Subcontracting).
    type_field = page.locator("div[name='type']").first
    kit_option = type_field.locator("label:has-text('Kit')").first
    if kit_option.count() == 0:
        kit_option = type_field.locator("input[value='phantom']").first
    kit_option.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # --- Add the two component lines under Components tab ---
    # The Components tab is the default tab on a fresh BoM form, so the
    # "Add a line" link is already visible. If another notebook tab was
    # auto-focused we'd need click_tab(page, 'Components') — keep it
    # defensive.
    try:
        # Make sure we're on the Components tab.
        comp_tab = page.locator(
            ".o_notebook .nav-link:has-text('Components')"
        ).first
        if comp_tab.count() > 0 and comp_tab.is_visible():
            comp_tab.click()
            page.wait_for_timeout(300)
    except Exception:
        pass

    click_add_a_line(page)
    set_o2m_many2one(page, 0, "product_id", COMP_A_NAME)
    set_o2m_field(page, 0, "product_qty", "2")

    click_add_a_line(page)
    set_o2m_many2one(page, 1, "product_id", COMP_B_NAME)
    set_o2m_field(page, 1, "product_qty", "3")

    save_form(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)


run_oracle(oracle)
