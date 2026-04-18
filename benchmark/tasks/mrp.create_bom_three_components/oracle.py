"""Oracle for mrp.create_bom_three_components.

Navigate to Manufacturing BoM list, create a new BoM for 'Wooden Chair'
with exactly 3 components, and save.
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


def oracle(page):
    login(page)

    navigate(page, "/odoo/action-mrp.mrp_bom_form_action")
    _wait_no_loading(page)
    click_create(page)
    _wait_for_ready(page)

    set_many2one(page, "product_tmpl_id", "Wooden Chair")
    fill_field(page, "product_qty", "1")

    click_add_a_line(page)
    set_o2m_many2one(page, 0, "product_id", "Wooden Leg")
    set_o2m_field(page, 0, "product_qty", "4")

    click_add_a_line(page)
    set_o2m_many2one(page, 1, "product_id", "Seat Board")
    set_o2m_field(page, 1, "product_qty", "1")

    click_add_a_line(page)
    set_o2m_many2one(page, 2, "product_id", "Backrest Panel")
    set_o2m_field(page, 2, "product_qty", "1")

    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
