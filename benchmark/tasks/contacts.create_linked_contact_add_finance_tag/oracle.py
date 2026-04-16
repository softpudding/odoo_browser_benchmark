"""Oracle for contacts.create_linked_contact_add_finance_tag."""

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

    person_radio = page.locator(
        "input[data-value='person'], "
        "div.o_field_radio[name='company_type'] .o_radio_item:has-text('Individual') input"
    )
    if person_radio.count() > 0 and not person_radio.first.is_checked():
        person_radio.first.click()
        page.wait_for_timeout(300)

    fill_field(page, "name", "Dana Patel")
    page.wait_for_timeout(300)
    set_many2one(page, "parent_id", "Lakeshore Manufacturing")
    page.wait_for_timeout(400)
    fill_field(page, "function", "Accounts Payable Specialist")
    page.wait_for_timeout(300)
    fill_field(page, "email", "dana.patel@lakeshore.example.com")
    page.wait_for_timeout(300)
    fill_field(page, "phone", "+1 312 555 0184")
    page.wait_for_timeout(300)
    fill_field(page, "street", "88 Harbor Way")
    page.wait_for_timeout(300)
    fill_field(page, "city", "Chicago")
    page.wait_for_timeout(300)
    set_many2one(page, "state_id", "Illinois")
    page.wait_for_timeout(300)
    fill_field(page, "zip", "60601")
    page.wait_for_timeout(300)
    set_many2one(page, "country_id", "United States")
    page.wait_for_timeout(300)
    add_many2many_tag(page, "category_id", "Finance")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(900)
    _wait_no_loading(page)


run_oracle(oracle)
