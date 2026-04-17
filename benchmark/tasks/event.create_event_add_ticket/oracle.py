"""Oracle for event.create_event_add_ticket."""

from benchmark.oracle_helpers import (
    click_create,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_boolean,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)

    click_create(page)
    _wait_for_ready(page)

    name_input = page.locator(
        ".o_field_widget[name='name'] textarea:visible, "
        ".o_field_widget[name='name'] input:visible"
    ).first
    name_input.click()
    name_input.fill("Operations Leadership Summit 2026")
    page.wait_for_timeout(300)

    page.locator(".o_daterange_start").first.click()
    page.wait_for_timeout(500)
    for _ in range(3):
        page.locator(".o_datetime_picker .o_next").first.click()
        page.wait_for_timeout(200)
    page.locator(".o_datetime_picker .o_date_item_cell:has-text('10')").first.click()
    page.wait_for_timeout(300)
    time_inputs = page.locator(".o_datetime_picker .o_time_picker_input:visible")
    time_inputs.nth(0).fill("09:00")
    time_inputs.nth(1).fill("17:00")
    page.locator(".o_datetime_picker .btn.btn-primary:has-text('Apply')").first.click()
    _wait_no_loading(page)

    set_boolean(page, "seats_limited", True)
    fill_field(page, "seats_max", "60")
    save_form(page)
    _wait_no_loading(page)

    click_tab(page, "Tickets")
    page.locator(
        "a.o_field_x2many_list_row_add:visible, td.o_field_x2many_list_row_add a:visible"
    ).first.click()
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "name", "Standard Pass")
    set_o2m_field(page, 0, "price", "199")
    set_o2m_field(page, 0, "seats_max", "50")

    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
