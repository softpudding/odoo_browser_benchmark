"""Oracle for sale.update_salesperson_validity_confirm."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, "S-QUOTE-VAL-01")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    edit_btn = page.locator(
        ".o_control_panel button:has-text('Edit'):visible, button.o_form_button_edit:visible"
    )
    if edit_btn.count() > 0:
        edit_btn.first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)

    set_date(page, "validity_date", "06/25/2026")
    page.wait_for_timeout(300)

    click_tab(page, "Other Info")
    page.wait_for_timeout(400)

    fill_field(page, "client_order_ref", "CGS-JUNE")
    page.wait_for_timeout(300)
    set_many2one(page, "user_id", "Marc Demo")
    page.wait_for_timeout(400)
    modal = page.locator(".modal:visible, .o_technical_modal:visible")
    if modal.count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
