"""Oracle for sale.update_quote_reference."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
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
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, "BENCH-QREF-01")
    _wait_for_ready(page)
    edit_btn = page.locator(
        ".o_control_panel button:has-text('Edit'):visible, button.o_form_button_edit:visible"
    )
    if edit_btn.count() > 0:
        edit_btn.first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)
    click_tab(page, "Other Info")
    page.wait_for_timeout(400)
    fill_field(page, "client_order_ref", "BENCH-QREF-01-UPDATED")
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
