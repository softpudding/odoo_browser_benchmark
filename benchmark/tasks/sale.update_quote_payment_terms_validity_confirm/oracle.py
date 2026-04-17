"""Oracle for sale.update_quote_payment_terms_validity_confirm."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    set_date,
    set_many2one,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    click_list_row(page, "BENCH-PMT-02")
    page.wait_for_timeout(500)
    set_many2one(page, "payment_term_id", "30 Net Days")
    page.wait_for_timeout(500)
    set_date(page, "validity_date", "05/28/2026")
    page.wait_for_timeout(500)
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    for i in range(rows.count()):
        if "Desk Organizer" in rows.nth(i).inner_text():
            set_o2m_field(page, i, "product_uom_qty", "12")
            break
    page.wait_for_timeout(500)
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
