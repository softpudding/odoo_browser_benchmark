"""Oracle for calendar.create_recurring_meeting_weekly_pattern.

Creates a weekly recurring calendar event 'Bench Weekly Standup' on Monday
2026-05-04 10:00-10:30 with recurrence configured via the UI:
  - rrule_type_ui = Weekly
  - Monday-only (calendar_week_days widget)
  - end_type = Number of repetitions
  - count = 4

Saves via breadcrumb. Oracle uses the same UI widget selectors documented in
calendar.schedule_recurring_steering_sync/oracle.py.
"""

from benchmark.oracle_helpers import (
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_boolean,
    _wait_no_loading,
    _wait_for_ready,
)


EVENT_NAME = "Bench Weekly Standup"


def _select_menu(page, field_name, label):
    """Select a value from an Odoo 19 SelectMenu widget."""
    widget = page.locator(f'.o_field_widget[name="{field_name}"]').first
    inp = widget.locator("input")
    if inp.count() > 0 and inp.first.is_visible():
        current = inp.first.input_value()
        if current.strip() == label:
            return
        inp.first.click()
        page.wait_for_timeout(300)
        inp.first.fill("")
        inp.first.fill(label)
        page.wait_for_timeout(500)
    else:
        btn = widget.locator("button, .dropdown-toggle")
        btn.first.click()
        page.wait_for_timeout(500)

    items = page.locator(
        ".dropdown-menu:visible .o-dropdown-item, "
        ".o_select_menu_menu:visible .o_select_menu_item"
    )
    item = items.filter(has_text=label)
    if item.count() > 0:
        item.first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _set_week_day(page, day_index, active):
    """Toggle a day in the calendar_week_days widget by 0-based visible index.

    For default US locale (weekStart=0/Sunday): 0=Sun 1=Mon 2=Tue 3=Wed 4=Thu
    5=Fri 6=Sat. The active state is the 'text-bg-action' class on the rounded
    button.
    """
    container = page.locator(".o_recurrent_weekdays").first
    day_buttons = container.locator(".o_calendar_week_days_rounded")
    btn = day_buttons.nth(day_index)
    is_active = "text-bg-action" in (btn.get_attribute("class") or "")
    if is_active != active:
        btn.click()
        page.wait_for_timeout(300)


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # New event
    page.locator('.o_control_panel button:has-text("New"):visible').first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Title
    fill_field(page, "name", EVENT_NAME)
    page.wait_for_timeout(400)

    # Start datetime — 05/04/2026 10:00:00 AM (admin tz forced to UTC by seed).
    start_input = page.locator('.o_field_widget[name="start"] input').first
    start_input.click()
    start_input.fill("")
    start_input.type("05/04/2026 10:00:00 AM")
    start_input.press("Tab")
    page.wait_for_timeout(800)
    if page.locator(".o_datetime_picker:visible").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)

    # Duration — 0.5h → stop = start + 30 min (cookbook: write duration directly).
    duration_input = page.locator('.o_field_widget[name="duration"] input').first
    duration_input.click(click_count=3)
    duration_input.fill("00:30")
    duration_input.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Recurrency lives on the Options tab (not the main form body).
    click_tab(page, "Options")
    page.wait_for_timeout(600)

    # Enable recurrence — triggers the recurrence panel on the Options tab.
    set_boolean(page, "recurrency", True)
    page.wait_for_timeout(1500)

    # rrule_type defaults to Weekly but set it explicitly to be robust.
    _select_menu(page, "rrule_type_ui", "Weekly")
    page.wait_for_timeout(500)

    # Make sure the weekday widget is rendered.
    page.wait_for_selector(".o_recurrent_weekdays", timeout=5000)
    page.wait_for_timeout(400)

    # Monday-only: deactivate all other days, activate Monday (index 1 in US locale).
    for i in range(7):
        _set_week_day(page, i, i == 1)
    page.wait_for_timeout(400)

    # End type → Number of repetitions.
    _select_menu(page, "end_type", "Number of repetitions")
    page.wait_for_timeout(500)

    # Count → 4
    fill_field(page, "count", "4")
    page.wait_for_timeout(500)

    # Save via breadcrumb.
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
