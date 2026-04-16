"""Oracle for contacts.update_company_with_supplier_tag."""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_list_row,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)

    click_list_row(page, "North Coast Fabrication")
    page.wait_for_timeout(300)
    fill_field(page, "phone", "+1 (206) 555-0184")
    page.wait_for_timeout(300)
    fill_field(page, "website", "www.northcoastfab.example.com")
    page.wait_for_timeout(300)
    fill_field(page, "street", "85 Harbor Way")
    page.wait_for_timeout(300)
    fill_field(page, "city", "Seattle")
    page.wait_for_timeout(300)
    set_many2one(page, "state_id", "Washington")
    page.wait_for_timeout(400)
    set_many2one(page, "country_id", "United States")
    page.wait_for_timeout(400)
    fill_field(page, "zip", "98134")
    page.wait_for_timeout(300)
    add_many2many_tag(page, "category_id", "Supplier")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
