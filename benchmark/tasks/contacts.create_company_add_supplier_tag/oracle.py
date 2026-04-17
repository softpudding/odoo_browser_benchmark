"""Oracle for contacts.create_company_add_supplier_tag."""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)

    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    company_radio = page.locator(
        "div.o_field_radio[name='company_type'] .o_radio_item:has-text('Company') input, "
        "input[value='company'], "
        ".o_field_widget[name='is_company'] input[type='checkbox']"
    ).first
    if company_radio.count() > 0:
        try:
            if not company_radio.is_checked():
                company_radio.click()
                page.wait_for_timeout(300)
        except Exception:
            company_radio.click()
            page.wait_for_timeout(300)

    fill_field(page, "name", "North Coast Fabrication")
    fill_field(page, "street", "1450 Harbor Rd")
    fill_field(page, "city", "Tacoma")
    fill_field(page, "zip", "98402")
    fill_field(page, "email", "ops@northcoastfab.com")
    fill_field(page, "phone", "+1 555 0182")
    fill_field(page, "website", "https://northcoastfab.com")
    add_many2many_tag(page, "category_id", "Supplier")

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
