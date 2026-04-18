"""Oracle for sale_management.create_quotation_template_apply_to_new_so.

Two-stage workflow:
 1. Sales > Configuration > Quotation Templates > New
    - Name: "Bench Starter Pack"
    - Two product lines: Bench Widget x5, Bench Gadget x2
    - Save.
 2. Sales > Orders > Quotations > New
    - Customer: "Bench Test Co"
    - Quotation Template: "Bench Starter Pack" (onchange auto-populates lines)
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

    # ---------- Stage 1: Create the quotation template ----------
    navigate(page, "/odoo/action-sale_management.sale_order_template_action")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    click_create(page)
    page.wait_for_timeout(800)

    # Template title (H1 header)
    fill_field(page, "name", "Bench Starter Pack")
    page.wait_for_timeout(400)

    # --- First line: Bench Widget, qty 5 ---
    click_add_a_line(page)
    page.wait_for_timeout(600)
    set_o2m_many2one(page, 0, "product_id", "Bench Widget")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    set_o2m_field(page, 0, "product_uom_qty", "5")
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # --- Second line: Bench Gadget, qty 2 ---
    click_add_a_line(page)
    page.wait_for_timeout(600)
    set_o2m_many2one(page, 1, "product_id", "Bench Gadget")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    set_o2m_field(page, 1, "product_uom_qty", "2")
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # Close any lingering dropdown before saving
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # ---------- Stage 2: Create the Sales Order that applies the template ----------
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    click_create(page)
    page.wait_for_timeout(800)

    # Customer — triggers default computes on partner-related fields
    set_many2one(page, "partner_id", "Bench Test Co")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Apply quotation template — _onchange_sale_order_template_id fills the
    # order lines automatically. The m2o field is rendered with
    # options="{'no_create': True}" so we cannot quick-create.
    set_many2one(page, "sale_order_template_id", "Bench Starter Pack")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Save (do not confirm)
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
