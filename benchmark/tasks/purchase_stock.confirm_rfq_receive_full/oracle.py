"""Oracle for purchase_stock.confirm_rfq_receive_full."""

from benchmark.oracle_helpers import (
    click_button_name,
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "MED-RECV-PO-01")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    click_button_name(page, "action_view_picking")
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    for i in range(rows.count()):
        row_text = rows.nth(i).inner_text()
        if "Steel Cable Reel" in row_text:
            set_o2m_field(page, i, "quantity", "12")
        elif "Safety Tape Pack" in row_text:
            set_o2m_field(page, i, "quantity", "30")
        page.wait_for_timeout(300)

    click_status_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Apply'), button:has-text('Ok'), button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
