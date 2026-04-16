"""Oracle for contacts.update_contact_phone."""

from benchmark.oracle_helpers import (
    click_list_row,
    ensure_list_view,
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

    ensure_list_view(page)
    click_list_row(page, "Nora Patel")
    _wait_for_ready(page)

    fill_field(page, "phone", "+1 555 0312")
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
