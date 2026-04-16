"""Oracle for contacts.create_company_add_supplier_finance_tags."""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
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
        if not company_radio.is_checked():
            company_radio.click()
            page.wait_for_timeout(300)
    else:
        page.locator("label:has-text('Company'), .o_radio_item:has-text('Company')").first.click()
        page.wait_for_timeout(300)

    fill_field(page, "name", "Harborview Components")
    fill_field(page, "phone", "+1 (415) 555-0148")
    fill_field(page, "website", "www.harborview-components.example.com")
    fill_field(page, "street", "245 Pier Avenue")
    fill_field(page, "city", "San Francisco")
    set_many2one(page, "state_id", "California")
    set_many2one(page, "country_id", "United States")
    fill_field(page, "zip", "94107")
    add_many2many_tag(page, "category_id", "Supplier")
    add_many2many_tag(page, "category_id", "Finance")

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
