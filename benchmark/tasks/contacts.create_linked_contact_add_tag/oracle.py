"""Oracle for contacts.create_linked_contact_add_tag."""

from benchmark.oracle_helpers import (
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

    person_radio = page.locator("input[data-value='person']").first
    if person_radio.count() > 0 and not person_radio.is_checked():
        person_radio.click()
        page.wait_for_timeout(300)

    fill_field(page, "name", "Leah Morgan")
    page.wait_for_timeout(300)
    set_many2one(page, "parent_id", "Seabird Logistics")
    page.wait_for_timeout(400)
    fill_field(page, "function", "Operations Coordinator")
    page.wait_for_timeout(300)
    fill_field(page, "email", "leah.morgan@seabird.example.com")
    page.wait_for_timeout(300)
    fill_field(page, "phone", "+1 415 555 0147")
    page.wait_for_timeout(300)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
