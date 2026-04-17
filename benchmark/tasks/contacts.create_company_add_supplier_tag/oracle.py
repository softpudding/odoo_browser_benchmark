"""Oracle for contacts.create_company_add_supplier_tag."""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)

    click_create(page)
    page.wait_for_timeout(900)
    _wait_for_ready(page)

    company_radio = page.locator("input[data-value='company']").first
    if company_radio.count() > 0 and not company_radio.is_checked():
        company_radio.click()
        page.wait_for_timeout(300)

    fill_field(page, "name", "North Coast Fabrication")
    page.wait_for_timeout(300)
    fill_field(page, "street", "1450 Harbor Rd")
    page.wait_for_timeout(300)
    fill_field(page, "city", "Tacoma")
    page.wait_for_timeout(300)
    fill_field(page, "zip", "98402")
    page.wait_for_timeout(300)
    fill_field(page, "email", "ops@northcoastfab.com")
    page.wait_for_timeout(300)
    fill_field(page, "phone", "+1 555 0182")
    page.wait_for_timeout(300)
    fill_field(page, "website", "https://northcoastfab.com")
    page.wait_for_timeout(300)
    add_many2many_tag(page, "category_id", "Supplier")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
