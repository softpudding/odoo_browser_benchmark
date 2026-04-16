"""Oracle for contacts.create_company_set_supplier_tag."""

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
        if not company_radio.is_checked():
            company_radio.click()
            page.wait_for_timeout(300)
    else:
        page.locator(
            "label:has-text('Company'), .o_radio_item:has-text('Company')"
        ).first.click()
        page.wait_for_timeout(300)

    fill_field(page, "name", "Harborview Fabrication")
    fill_field(page, "email", "ops@harborview.example.com")
    fill_field(page, "phone", "+1 206 555 0144")
    fill_field(page, "website", "https://harborview.example.com")
    add_many2many_tag(page, "category_id", "Supplier")

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
