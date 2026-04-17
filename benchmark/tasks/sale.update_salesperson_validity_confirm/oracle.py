"""Oracle for sale.update_salesperson_validity_confirm."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_date,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def _set_many2one_any(page, field_name: str, search_text: str) -> None:
    widget = page.locator(f".o_field_widget[name='{field_name}']").first
    inp = widget.locator("input:visible, .o-autocomplete--input:visible").first
    inp.click()
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(800)
    page.locator(
        ".dropdown-menu:visible .dropdown-item, .ui-autocomplete .ui-menu-item"
    ).filter(has_text=search_text).first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, "S-QUOTE-VAL-01")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    set_date(page, "validity_date", "06/25/2026")
    page.wait_for_timeout(500)
    click_tab(page, "Other Info")
    page.wait_for_timeout(400)
    _set_many2one_any(page, "user_id", "Marc Demo")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "CGS-JUNE")
    page.wait_for_timeout(500)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
