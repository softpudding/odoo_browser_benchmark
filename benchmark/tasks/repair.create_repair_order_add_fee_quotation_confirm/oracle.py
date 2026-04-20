"""Oracle for repair.create_repair_order_add_fee_quotation_confirm."""
from benchmark.oracle_helpers import (
    click_button,
    click_create,
    click_status_button,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
)

def oracle(page):
    login(page)
    navigate(page, "/odoo/repairs")
    click_create(page)
    set_many2one(page, "partner_id", "Repair Harbor")
    set_many2one(page, "product_id", "Bench Pump Core")
    click_tab(page, "Parts")
    page.locator(
        "div[name='move_ids'] a.o_field_x2many_list_row_add:visible, "
        "div[name='move_ids'] td.o_field_x2many_list_row_add a:visible"
    ).first.click()
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 0, "product_id", "Bench Diagnostic Fee")
    set_o2m_field(page, 0, "product_uom_qty", "1")
    save_form(page)
    click_button(page, "Create Quotation")
    click_status_button(page, "Confirm")

run_oracle(oracle)
