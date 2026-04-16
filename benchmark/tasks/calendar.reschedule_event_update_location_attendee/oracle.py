"""Oracle for calendar.reschedule_event_update_location_attendee."""

from benchmark.oracle_helpers import (
    add_many2many_tag,
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
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    event = page.locator(".fc-event:has-text('Warehouse Safety Briefing')").first
    if event.count() == 0:
        next_btn = page.locator(".o_calendar_button_next").first
        if next_btn.count() > 0:
            next_btn.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)
        event = page.locator(".fc-event:has-text('Warehouse Safety Briefing')").first

    event.click()
    page.wait_for_timeout(600)

    edit_link = page.locator("a.o_cw_popover_edit, a:has-text('Edit')").first
    if edit_link.count() > 0:
        edit_link.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    fill_field(page, "location", "Training Room")
    page.wait_for_timeout(400)
    add_many2many_tag(page, "partner_ids", "Marc Demo")
    page.wait_for_timeout(600)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
