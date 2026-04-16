"""Oracle for purchase.update_rfq_reference_deadline_confirm."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "MED-RFQ-REF-01")
    page.wait_for_timeout(800)

    fill_field(page, "partner_ref", "NCC-8842")
    page.wait_for_timeout(400)
    set_date(page, "date_order", "05/22/2026")
    page.wait_for_timeout(400)
    set_o2m_field(page, 0, "product_qty", "24")
    page.wait_for_timeout(500)
    save_form(page)
    page.wait_for_timeout(700)

    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
