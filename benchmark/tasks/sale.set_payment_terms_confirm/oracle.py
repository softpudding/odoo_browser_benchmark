"""Oracle for sale.set_payment_terms_confirm.

Find draft quotation BENCH-PMT-01 for Azure Interior. Set payment terms
to "30 Net Days", change Desk Organizer qty from 5 to 12, update customer
reference to "AZ-2026-Q2", and confirm.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the quotation
    click_list_row(page, "BENCH-PMT-01")
    page.wait_for_timeout(500)

    # Set payment terms (on main Order Lines tab)
    set_many2one(page, "payment_term_id", "30 Net Days")
    page.wait_for_timeout(500)

    # Find the Desk Organizer row and change quantity to 12
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    for i in range(rows.count()):
        row_text = rows.nth(i).inner_text()
        if "Desk Organizer" in row_text:
            set_o2m_field(page, i, "product_uom_qty", "12")
            break
    page.wait_for_timeout(500)

    # Customer Reference is on the "Other Info" tab
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "AZ-2026-Q2")
    page.wait_for_timeout(500)

    # Confirm the quotation
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
