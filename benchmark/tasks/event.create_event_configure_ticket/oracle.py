"""Oracle for event.create_event_configure_ticket."""

from benchmark.oracle_helpers import (
    click_create,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_boolean,
    set_many2one,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    click_create(page)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Fill event name (textarea in Odoo 19).
    name_input = page.locator(
        ".o_field_widget[name='name'] textarea:visible, "
        ".o_field_widget[name='name'] input:visible"
    ).first
    name_input.click()
    name_input.fill("Spring Tech Conference 2026")
    page.wait_for_timeout(300)

    # Open the date range picker and choose 04/15/2026 09:00 → 04/16/2026 17:00.
    page.locator(".o_daterange_start").first.click()
    page.wait_for_timeout(600)

    # Navigate forward to April 2026 (from today). Click next until we see April 2026.
    for _ in range(24):
        header = page.locator(".o_datetime_picker .o_datetime_picker_header").first
        text = header.inner_text() if header.count() > 0 else ""
        if "April" in text and "2026" in text:
            break
        page.locator(".o_datetime_picker .o_next").first.click()
        page.wait_for_timeout(150)

    # Pick day 15 for start.
    page.locator(
        ".o_datetime_picker .o_date_item_cell:not(.o_out_of_range):has-text('15')"
    ).first.click()
    page.wait_for_timeout(300)
    # Pick day 16 for end.
    page.locator(
        ".o_datetime_picker .o_date_item_cell:not(.o_out_of_range):has-text('16')"
    ).first.click()
    page.wait_for_timeout(300)

    time_inputs = page.locator(".o_datetime_picker .o_time_picker_input:visible")
    # Set start time 09:00 and end time 17:00.
    time_inputs.nth(0).fill("09:00")
    page.wait_for_timeout(150)
    time_inputs.nth(1).fill("17:00")
    page.wait_for_timeout(150)

    # Apply the date picker.
    apply_btn = page.locator(
        ".o_datetime_picker .btn.btn-primary:has-text('Apply')"
    )
    if apply_btn.count() > 0:
        apply_btn.first.click()
    else:
        page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # Set Location (address_id) to Riverside Convention Center.
    set_many2one(page, "address_id", "Riverside Convention Center")
    page.wait_for_timeout(300)

    # Go to Tickets tab and add one ticket row.
    click_tab(page, "Tickets")
    page.wait_for_timeout(500)

    add_line = page.locator(
        "div[name='event_ticket_ids'] a:has-text('Add a line'), "
        "div[name='event_ticket_ids'] button:has-text('Add a line'), "
        "div[name='event_ticket_ids'] a.o_field_x2many_list_row_add, "
        ".o_field_x2many[name='event_ticket_ids'] a:has-text('Add a line')"
    ).first
    add_line.wait_for(state="visible", timeout=15000)
    add_line.click()
    page.wait_for_timeout(500)

    set_o2m_field(page, 0, "name", "Standard Pass")
    set_o2m_field(page, 0, "price", "150.00")

    # The seats limit on ticket is an integer (seats_max) with a boolean
    # (seats_limited). In the list view the optional column may need to be
    # enabled, but seats_max is typically inline. Fill it directly.
    set_o2m_field(page, 0, "seats_max", "100")
    page.wait_for_timeout(300)

    save_form(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)


run_oracle(oracle)
