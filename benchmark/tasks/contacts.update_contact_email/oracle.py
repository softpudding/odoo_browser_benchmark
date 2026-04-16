"""Oracle for contacts.update_contact_email."""

from benchmark.oracle_helpers import (
    click_list_row,
    fill_field,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)

    click_list_row(page, "Avery Dalton")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    fill_field(page, "email", "avery.dalton+ops@example.com")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
