"""Oracle for contacts.update_contact_mobile."""

from benchmark.oracle_helpers import (
    click_list_row,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
    ensure_list_view,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)

    ensure_list_view(page)
    click_list_row(page, "Milo Reyes")
    _wait_for_ready(page)

    fill_field(page, "website", "https://www.miloreyes.example.com")
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
