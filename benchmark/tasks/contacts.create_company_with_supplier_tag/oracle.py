"""Oracle for contacts.create_company_with_supplier_tag."""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
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
        except Exception:
            company_radio.click()
        page.wait_for_timeout(300)
    else:
        page.locator("label:has-text('Company'), .o_radio_item:has-text('Company')").first.click()
        page.wait_for_timeout(300)

    fill_field(page, "name", "North Coast Fabrication")
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
