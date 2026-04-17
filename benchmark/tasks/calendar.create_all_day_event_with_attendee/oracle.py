"""Oracle for calendar.create_all_day_event_with_attendee."""

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

    scale_btn = page.locator(".scale_button_selection").first
    if scale_btn.count() > 0:
        scale_btn.click()
        page.wait_for_timeout(500)
        month_item = page.locator(
            ".dropdown-menu:visible .dropdown-item:has-text('Month')"
        ).first
        if month_item.count() > 0:
            month_item.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)

    for _ in range(12):
        day_cell = page.locator(
            ".fc-daygrid-day[data-date='2026-06-18'], .fc-day[data-date='2026-06-18']"
        ).first
        if day_cell.count() > 0 and day_cell.is_visible():
            break
        page.locator(".o_calendar_button_next").first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)

    day_frame = page.locator(
        ".fc-daygrid-day[data-date='2026-06-18'] .fc-daygrid-day-frame, "
        ".fc-day[data-date='2026-06-18']"
    ).first
    day_frame.click()
    page.wait_for_timeout(1000)

    modal = page.locator(".modal:visible").last
    modal.locator(".o_field_widget[name='name'] input").first.fill("Operations Offsite")
    page.wait_for_timeout(400)
    modal.locator("button:has-text('More Options')").first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    fill_field(page, "location", "Mountain View Campus")
    page.wait_for_timeout(400)
    add_many2many_tag(page, "partner_ids", "Marc Demo")
    page.wait_for_timeout(400)

    click_tab(page, "Options")
    page.wait_for_timeout(400)
    desc = page.locator(
        '.o_field_widget[name="description"] .note-editable, '
        '.o_field_widget[name="description"] .odoo-editor-editable, '
        '.o_field_widget[name="description"] [contenteditable="true"]'
    ).first
    desc.click()
    page.keyboard.insert_text("Annual planning offsite for operations leads.")
    page.wait_for_timeout(500)

    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
