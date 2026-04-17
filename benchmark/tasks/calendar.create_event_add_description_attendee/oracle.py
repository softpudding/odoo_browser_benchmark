"""Oracle for calendar.create_event_add_description_attendee."""

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

    page.locator('.o_control_panel button:has-text("New"):visible').first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    fill_field(page, "name", "Vendor Kickoff Briefing")
    page.wait_for_timeout(500)

    start_input = page.locator('.o_field_widget[name="start"] input').first
    start_input.click()
    start_input.fill("")
    start_input.type("05/22/2026 11:00:00 AM")
    start_input.press("Tab")
    page.wait_for_timeout(800)
    if page.locator(".o_datetime_picker:visible").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)

    stop_btn = page.locator(".o_daterange_end").first
    stop_btn.click()
    page.wait_for_timeout(1000)
    time_inputs = page.locator(".o_datetime_picker:visible .o_time_picker_input")
    if time_inputs.count() >= 2:
        end_time_input = time_inputs.nth(1)
        end_time_input.click(click_count=3)
        end_time_input.fill("12:30pm")
        end_time_input.press("Tab")
        page.wait_for_timeout(500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    fill_field(page, "location", "Room 204")
    page.wait_for_timeout(500)
    add_many2many_tag(page, "partner_ids", "Marc Demo")
    page.wait_for_timeout(500)

    click_tab(page, "Options")
    page.wait_for_timeout(500)
    desc_editable = page.locator(
        '.o_field_widget[name="description"] .note-editable, '
        '.o_field_widget[name="description"] .odoo-editor-editable, '
        '.o_field_widget[name="description"] [contenteditable="true"]'
    ).first
    desc_editable.click()
    page.keyboard.type("Review kickoff agenda and confirm owners for the vendor rollout.")
    page.wait_for_timeout(500)

    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
