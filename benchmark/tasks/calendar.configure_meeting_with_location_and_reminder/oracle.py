"""Oracle for calendar.configure_meeting_with_location_and_reminder.

Creates the calendar.event via the UI flow: opens Calendar, clicks New, fills
name/start/stop/location, adds the two seeded internal-user attendees via the
partner_ids many2many_tags autocomplete, switches to the Options tab, adds the
pre-existing ``Notification - 1 Hours`` calendar.alarm to the alarm_ids
many2many_tags autocomplete, and saves by navigating via the breadcrumb.

Notes:
  - Admin tz is NOT UTC in benchmark_base (documented cookbook quirk). The
    ``05/22/2026 11:00:00 AM`` format in Odoo's datetime input is interpreted
    in the admin's tz, so typing local time directly gives the right stored
    UTC value.
  - ``location`` sits on the main event form (not in a tab) as a plain Char.
  - ``alarm_ids`` is on the Options tab as a many2many_tags with
    ``no_quick_create=True`` -- the agent must pick an existing alarm.
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
)


EVENT_NAME = "Quarterly Review"
LOCATION = "Conference Room B, Floor 3"
ATTENDEES = ("Alice Attendee", "Bob Attendee")
ALARM_TAG = "Notification - 1 Hours"


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    page.locator('.o_control_panel button:has-text("New"):visible').first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    fill_field(page, "name", EVENT_NAME)
    page.wait_for_timeout(500)

    # Start datetime.
    start_input = page.locator('.o_field_widget[name="start"] input').first
    start_input.click()
    start_input.fill("")
    start_input.type("06/10/2026 02:00:00 PM")
    start_input.press("Tab")
    page.wait_for_timeout(800)
    if page.locator(".o_datetime_picker:visible").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)

    # Set duration to 2.0 hours directly (stop computes from start + duration).
    duration_input = page.locator('.o_field_widget[name="duration"] input').first
    duration_input.click(click_count=3)
    duration_input.fill("02:00")
    duration_input.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Location (plain Char on the main form).
    fill_field(page, "location", LOCATION)
    page.wait_for_timeout(400)

    # Attendees via partner_ids many2many_tags.
    for name in ATTENDEES:
        add_many2many_tag(page, "partner_ids", name)
        page.wait_for_timeout(300)

    # Switch to Options tab and add the 1-hour reminder.
    click_tab(page, "Options")
    page.wait_for_timeout(600)
    add_many2many_tag(page, "alarm_ids", ALARM_TAG)
    page.wait_for_timeout(500)

    # Save via breadcrumb (matches reference oracle pattern).
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
