"""Oracle for event.create_event_mail_schedule_and_publish_registration."""
from benchmark.oracle_helpers import (
    _wait_no_loading,
    _wait_for_ready,
    click_create,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
)

def set_row_select_menu(row, field_name, value):
    cell = row.locator(f"td[name='{field_name}']").first
    inp = cell.locator("input.o_select_menu_input").first
    inp.click()
    inp.fill("")
    inp.fill(value)
    cell.page.wait_for_timeout(500)
    cell.page.locator(
        ".o-overlay-container .dropdown-item, .dropdown-menu .dropdown-item"
    ).filter(has_text=value).first.click()
    cell.page.wait_for_timeout(300)

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
    name_input.fill("Dock Systems Expo 2026")
    page.wait_for_timeout(300)

    page.locator(".o_daterange_start").first.click()
    page.wait_for_timeout(600)
    for _ in range(24):
        header = page.locator(".o_datetime_picker .o_datetime_picker_header").first
        text = header.inner_text() if header.count() > 0 else ""
        if "July" in text and "2026" in text:
            break
        page.locator(".o_datetime_picker .o_next").first.click()
        page.wait_for_timeout(150)

    page.locator(
        ".o_datetime_picker .o_date_item_cell:not(.o_out_of_range):has-text('10')"
    ).first.click()
    page.wait_for_timeout(300)
    time_inputs = page.locator(".o_datetime_picker .o_time_picker_input:visible")
    time_inputs.nth(0).fill("09:00")
    time_inputs.nth(1).fill("17:00")
    page.locator(".o_datetime_picker .btn.btn-primary:has-text('Apply')").first.click()
    _wait_no_loading(page)

    click_tab(page, "Communication")
    for _ in range(page.locator(".o_form_view .o_list_renderer .o_data_row").count()):
        page.locator(".o_form_view .o_list_renderer .o_data_row .o_list_record_remove button[name='delete']").first.click()
        page.wait_for_timeout(300)
    page.locator(
        "div[name='event_mail_ids'] a.o_field_x2many_list_row_add:visible, "
        "div[name='event_mail_ids'] td.o_field_x2many_list_row_add a:visible"
    ).first.click()
    page.wait_for_timeout(500)
    row = page.locator(".o_form_view .o_list_renderer .o_data_row").last
    row.locator("td[name='template_ref']").click()
    page.wait_for_timeout(300)
    row.locator("td[name='template_ref'] input").fill("Bench Event Reminder")
    page.wait_for_timeout(800)
    page.locator(".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item").filter(
        has_text="Bench Event Reminder"
    ).first.click()
    page.wait_for_timeout(500)
    row.locator("td[name='interval_nbr'] input").fill("2")
    row.locator("td[name='interval_nbr'] input").press("Tab")
    page.wait_for_timeout(300)
    set_row_select_menu(row, "interval_unit", "Days")
    set_row_select_menu(row, "interval_type", "Before the event starts")
    page.wait_for_timeout(500)

    save_form(page)
    page.locator(
        ".oe_stat_button:has-text('Go to'):visible, "
        "button:has-text('Go to'):visible, "
        "a:has-text('Go to'):visible"
    ).first.click()
    page.wait_for_timeout(1500)
    publish_toggle = page.locator(".o_website_publish_container:visible, .o_menu_systray_item:has-text('Unpublished'):visible").first
    publish_toggle.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

run_oracle(oracle)
