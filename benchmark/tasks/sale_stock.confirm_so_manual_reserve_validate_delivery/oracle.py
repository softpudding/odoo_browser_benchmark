"""Oracle for sale_stock.confirm_so_manual_reserve_validate_delivery."""

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    clear_search_filters,
    click_button,
    click_list_row,
    click_stat_button,
    click_status_button,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    set_o2m_field,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(800)

    row = page.locator(
        ".o_list_view .o_data_row:has-text('Northwind Assembly')"
    ).first
    if row.count() > 0:
        customer_cell = row.locator(
            "td[name='partner_id'], td:has-text('Northwind Assembly')"
        ).first
        customer_cell.click(force=True)
        page.wait_for_load_state("load")
    else:
        click_list_row(page, "Northwind Assembly")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    click_stat_button(page, "Delivery")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_button(page, "Check Availability")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    for i in range(rows.count()):
        row_text = rows.nth(i).inner_text()
        if "Bench Servo Housing" in row_text:
            set_o2m_field(page, i, "quantity", "7")
            page.wait_for_timeout(300)
        elif "Bench Control Cable" in row_text:
            set_o2m_field(page, i, "quantity", "5")
            page.wait_for_timeout(300)

    click_status_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Apply'), "
            "button:has-text('Validate'), "
            "button:has-text('Ok'), "
            "button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
