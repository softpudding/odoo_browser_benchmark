"""Oracle for mrp.create_bom_confirm_mo."""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    click_status_button,
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

    navigate(page, "/odoo/boms")
    _wait_no_loading(page)
    click_create(page)
    _wait_for_ready(page)

    set_many2one(page, "product_tmpl_id", "BenchMaster Assembly Kit")
    fill_field(page, "code", "BM-KIT-26")
    fill_field(page, "product_qty", "1")

    click_add_a_line(page)
    set_o2m_many2one(page, 0, "product_id", "BenchMaster Frame")
    set_o2m_field(page, 0, "product_qty", "2")

    click_add_a_line(page)
    set_o2m_many2one(page, 1, "product_id", "BenchMaster Panel")
    set_o2m_field(page, 1, "product_qty", "4")

    click_add_a_line(page)
    set_o2m_many2one(page, 2, "product_id", "BenchMaster Fastener Pack")
    set_o2m_field(page, 2, "product_qty", "1")

    save_form(page)
    _wait_no_loading(page)

    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)
    click_create(page)
    _wait_for_ready(page)

    set_many2one(page, "product_id", "BenchMaster Assembly Kit")
    fill_field(page, "product_qty", "10")
    save_form(page)
    _wait_no_loading(page)

    click_status_button(page, "Confirm")
    _wait_no_loading(page)


run_oracle(oracle)
