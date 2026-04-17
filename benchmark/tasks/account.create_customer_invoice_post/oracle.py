"""Oracle for account.create_customer_invoice_post."""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    click_status_button,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_date,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def _click_add_line(page):
    click_add_a_line(page)
    page.wait_for_timeout(300)


def _add_line(page, row_idx: int, product: str, qty: str, price: str) -> None:
    _click_add_line(page)
    set_o2m_many2one(page, row_idx, "product_id", product)
    page.wait_for_timeout(300)
    set_o2m_field(page, row_idx, "quantity", qty)
    page.wait_for_timeout(300)
    set_o2m_field(page, row_idx, "price_unit", price)
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    click_create(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    set_many2one(page, "partner_id", "Northwind Advisory")
    page.wait_for_timeout(400)
    set_date(page, "invoice_date", "06/10/2026")
    page.wait_for_timeout(400)
    try:
        fill_field(page, "ref", "NWA-AR-220")
    except Exception:
        click_tab(page, "Other Info")
        page.wait_for_timeout(400)
        fill_field(page, "ref", "NWA-AR-220")
    page.wait_for_timeout(400)
    click_tab(page, "Invoice Lines")
    page.wait_for_timeout(400)

    _add_line(page, 0, "Strategic Workshop", "2", "1200")
    _add_line(page, 1, "Support Retainer", "1", "850")
    page.wait_for_timeout(500)
    page.locator(".o_form_sheet").first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
