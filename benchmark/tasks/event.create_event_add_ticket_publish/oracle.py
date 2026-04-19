"""Oracle for event.create_event_add_ticket_publish.

Pure Playwright UI oracle. Steps:

1. Navigate to /odoo/events and click New.
2. Fill the Event Name.
3. Open the daterange picker and pick 06/15/2026 09:00 -> 17:00 local
   (admin TZ is UTC+8, so the UI local wall-clock matches the prompt
   directly; Odoo stores it as UTC internally).
4. Save the event.
5. Switch to the Tickets tab, add a line with name 'General Admission'
   and price 50.00, save.
6. Click "Go to Website" on the form (the `website_redirect_button`
   widget bound to `is_published` — it only navigates, it does NOT
   toggle the publish state). On the frontend event page, click the
   Owl website systray switch to flip is_published to True.
"""

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    click_create,
    click_add_a_line,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_o2m_field,
)


EVENT_NAME = "Bench Summer Summit 2026"
TICKET_NAME = "General Admission"
TICKET_PRICE = "50.00"


def _pick_event_dates(page):
    """Open the event's daterange picker and set 06/15/2026 09:00 -> 17:00.

    Admin TZ is UTC+8, so the UI local wall-clock values match the
    prompt's declared times directly. A single click on a date cell in
    the range picker defaults end_date=start_date, which is what we want
    for this same-day event.
    """
    page.locator(".o_daterange_start").first.click()
    page.wait_for_timeout(600)

    # Navigate the calendar to June 2026. The header shows the current month.
    for _ in range(36):
        header = page.locator(".o_datetime_picker .o_datetime_picker_header").first
        text = header.inner_text() if header.count() > 0 else ""
        if "June" in text and "2026" in text:
            break
        page.locator(".o_datetime_picker .o_next").first.click()
        page.wait_for_timeout(150)

    # Click day 15 for the start date. A single click on a date cell in
    # the range picker defaults end=start, so we only need one click.
    page.locator(
        ".o_datetime_picker .o_date_item_cell:not(.o_out_of_range):has-text('15')"
    ).first.click()
    page.wait_for_timeout(400)

    time_inputs = page.locator(".o_datetime_picker .o_time_picker_input:visible")
    # Clear and set start time 09:00.
    time_inputs.nth(0).click()
    time_inputs.nth(0).fill("")
    time_inputs.nth(0).type("09:00")
    time_inputs.nth(0).press("Tab")
    page.wait_for_timeout(200)
    # Clear and set end time 17:00.
    time_inputs = page.locator(".o_datetime_picker .o_time_picker_input:visible")
    time_inputs.nth(1).click()
    time_inputs.nth(1).fill("")
    time_inputs.nth(1).type("17:00")
    time_inputs.nth(1).press("Tab")
    page.wait_for_timeout(200)

    apply_btn = page.locator(
        ".o_datetime_picker .btn.btn-primary:has-text('Apply')"
    )
    if apply_btn.count() > 0:
        apply_btn.first.click()
    else:
        page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Step 1: create the event.
    click_create(page)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    name_input = page.locator(
        ".o_field_widget[name='name'] textarea:visible, "
        ".o_field_widget[name='name'] input:visible"
    ).first
    name_input.click()
    name_input.fill(EVENT_NAME)
    page.wait_for_timeout(300)

    _pick_event_dates(page)

    save_form(page)
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Step 2: add a single ticket line in the Tickets tab.
    click_tab(page, "Tickets")
    page.wait_for_timeout(500)

    click_add_a_line(page)
    page.wait_for_timeout(500)

    set_o2m_field(page, 0, "name", TICKET_NAME)
    set_o2m_field(page, 0, "price", TICKET_PRICE)

    save_form(page)
    _wait_no_loading(page)
    page.wait_for_timeout(600)

    # Step 3: publish the event via the website systray.
    #
    # The event form's `is_published` field is rendered as a
    # `website_redirect_button` widget (the "Go to Website" globe button) —
    # it only navigates, it does NOT toggle the publish state. The
    # canonical UI path is to click that button to land on the frontend
    # event page, where the admin shell shows a website systray with an
    # "Unpublished / Published" switch that flips `is_published`.
    go_website = page.locator(
        ".o_field_widget[name='is_published'] button"
    ).first
    go_website.wait_for(state="visible", timeout=15000)
    go_website.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    # Wait for the Owl systray switch to mount on the frontend page.
    switch_selector = (
        ".o_menu_systray input[type='checkbox'], "
        ".o_website_publish_container input[type='checkbox'], "
        "input#website_publish_switch, "
        ".o_website_publish_container .form-switch input"
    )
    try:
        page.wait_for_selector(switch_selector, timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(500)

    # Toggle the systray publish switch (checkbox input inside
    # .o_menu_systray). Fall back to clicking the form-switch container
    # if the checkbox itself is not directly clickable.
    publish_switch = page.locator(switch_selector)
    if publish_switch.count() > 0:
        try:
            checked = publish_switch.first.is_checked()
        except Exception:
            checked = False
        if not checked:
            try:
                publish_switch.first.click()
            except Exception:
                page.locator(
                    ".o_menu_systray .form-switch, "
                    ".o_website_publish_container, "
                    ".o_menu_systray label"
                ).first.click()
            page.wait_for_timeout(1500)

    page.wait_for_timeout(500)


run_oracle(oracle)
