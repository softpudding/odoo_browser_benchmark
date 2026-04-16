"""Oracle for calendar.create_single_event.

Create a one-time calendar event "Q2 Strategy Review" on May 8, 2026,
2-4 PM, with location, description, and Marc Demo as attendee.
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Click New to create a new event (opens full form)
    page.locator(
        '.o_control_panel button:has-text("New"):visible'
    ).first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Set title
    fill_field(page, "name", "Q2 Strategy Review")
    page.wait_for_timeout(500)

    # Start datetime — renders as <input> for a new event
    start_input = page.locator('.o_field_widget[name="start"] input').first
    start_input.click()
    start_input.fill("")
    start_input.type("05/08/2026 02:00:00 PM")
    start_input.press("Tab")
    page.wait_for_timeout(800)
    # Close any opened picker
    picker = page.locator(".o_datetime_picker:visible")
    if picker.count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)

    # End time — click the daterange end button to open picker, then set time
    stop_btn = page.locator(".o_daterange_end").first
    stop_btn.click()
    page.wait_for_timeout(1000)

    time_inputs = page.locator(
        ".o_datetime_picker:visible .o_time_picker_input"
    )
    if time_inputs.count() >= 2:
        end_time_input = time_inputs.nth(1)
        end_time_input.click(click_count=3)
        end_time_input.fill("4:00pm")
        end_time_input.press("Tab")
        page.wait_for_timeout(500)

    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # Location
    fill_field(page, "location", "Conference Room A")
    page.wait_for_timeout(500)

    # Attendee Marc Demo
    add_many2many_tag(page, "partner_ids", "Marc Demo")
    page.wait_for_timeout(500)

    # Switch to Options tab for description
    click_tab(page, "Options")
    page.wait_for_timeout(500)

    desc_editable = page.locator(
        '.o_field_widget[name="description"] .note-editable, '
        '.o_field_widget[name="description"] .odoo-editor-editable, '
        '.o_field_widget[name="description"] [contenteditable="true"]'
    ).first
    desc_editable.click()
    page.keyboard.type(
        "Review Q2 objectives and align on priorities for the team."
    )
    page.wait_for_timeout(500)

    # Save by navigating back via breadcrumb
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
