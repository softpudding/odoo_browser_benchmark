"""Oracle for calendar.create_meeting_invite_attendees_send.

Creates the calendar.event via the UI flow: opens Calendar, clicks New, fills
name/start, sets duration=1:00 (so stop = start + 1h — cookbook-reliable
technique vs the flaky .o_daterange_end picker), adds the two seeded partners
Attendee Alpha + Attendee Beta via the partner_ids many2many_tags autocomplete,
and saves via the breadcrumb.

Notes:
  - Admin tz is NOT necessarily UTC in benchmark_base. The "05/20/2026
    10:00:00 AM" format in Odoo's datetime input is interpreted in the admin's
    tz, so typing local time directly gives the right stored UTC value; the
    check.py uses pytz to convert UTC → admin tz and compare local date/hour.
  - partner_ids is many2many_tags; the two seeded res.partner records satisfy
    autocomplete selection by exact name.
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    fill_field,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
)


EVENT_NAME = "Team Sync"
ATTENDEES = ("Attendee Alpha", "Attendee Beta")


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    page.locator('.o_control_panel button:has-text("New"):visible').first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    fill_field(page, "name", EVENT_NAME)
    page.wait_for_timeout(500)

    # Start datetime (admin-local tz interpretation).
    start_input = page.locator('.o_field_widget[name="start"] input').first
    start_input.click()
    start_input.fill("")
    start_input.type("05/20/2026 10:00:00 AM")
    start_input.press("Tab")
    page.wait_for_timeout(800)
    if page.locator(".o_datetime_picker:visible").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)

    # Set duration to 1.0 hour directly (stop computes from start + duration).
    duration_input = page.locator('.o_field_widget[name="duration"] input').first
    duration_input.click(click_count=3)
    duration_input.fill("01:00")
    duration_input.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Attendees via partner_ids many2many_tags.
    for name in ATTENDEES:
        add_many2many_tag(page, "partner_ids", name)
        page.wait_for_timeout(300)

    # Save via breadcrumb (matches reference oracle pattern).
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
