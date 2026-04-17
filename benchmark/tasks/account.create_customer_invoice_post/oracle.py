"""Oracle for account.create_customer_invoice_post."""

from benchmark.oracle_helpers import (
    click_button,
    click_tab,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def _enable_product_column(page):
    gear = page.locator(
        ".o_field_one2many[name='invoice_line_ids'] "
        ".o_optional_columns_dropdown_toggle"
    ).first
    gear.click()
    page.wait_for_timeout(500)

    product_item = page.locator(
        ".dropdown-menu:visible .dropdown-item"
    ).filter(has_text="Product").first
    checkbox = product_item.locator("input[type='checkbox']")
    if checkbox.count() == 0 or not checkbox.first.is_checked():
        product_item.click()
        page.wait_for_timeout(500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    _wait_no_loading(page)


def _click_add_line(page):
    page.locator(
        ".o_field_one2many[name='invoice_line_ids'] a"
    ).filter(has_text="Add a line").first.click()
    page.wait_for_timeout(800)


def _add_line(page, row_idx: int, product: str, qty: str, price: str) -> None:
    _click_add_line(page)
    set_o2m_many2one(page, row_idx, "product_id", product)
    page.wait_for_timeout(500)
    set_o2m_field(page, row_idx, "quantity", qty)
    page.wait_for_timeout(300)
    set_o2m_field(page, row_idx, "price_unit", price)
    page.wait_for_timeout(500)
    page.locator(".o_form_sheet").first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    set_many2one(page, "partner_id", "Northwind Advisory")
    page.wait_for_timeout(500)
    invoice_date = page.locator(".o_field_widget[name='invoice_date']").first
    invoice_input = invoice_date.locator("input:visible")
    if invoice_input.count() > 0:
        invoice_input.first.click()
        invoice_input.first.fill("")
        invoice_input.first.type("06/10/2026")
        invoice_input.first.press("Tab")
    else:
        set_date(page, "invoice_date", "06/10/2026")
    page.wait_for_timeout(500)

    _enable_product_column(page)
    _add_line(page, 0, "Strategic Workshop", "2", "1200")
    _add_line(page, 1, "Support Retainer", "1", "850")

    page.locator(".o_form_sheet").first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "ref", "NWA-AR-220")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
