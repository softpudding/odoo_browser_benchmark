"""Oracle for calendar.create_recurring_edit_two_occurrences.

Create a weekly recurring "Cross-Team Sync" event starting June 4 2026
10:00-11:00, location "Main Conference Room", invite Marc Demo, 6
occurrences. Then edit two individual occurrences:
  - June 11: change location to "Virtual - Zoom" (This Event only)
  - June 25: change location to "Building B Room 201" (This Event only)
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_boolean,
    _wait_no_loading,
    _wait_for_ready,
)


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
    """Toggle a day in the calendar_week_days widget.

    day_index: 0-based from locale week start.
    For US locale (weekStart=Sunday): 0=Sun,1=Mon,2=Tue,3=Wed,4=Thu,5=Fri,6=Sat
    """
    container = page.locator(".o_recurrent_weekdays").first
    day_buttons = container.locator(".o_calendar_week_days_rounded")
    btn = day_buttons.nth(day_index)
    is_active = "text-bg-action" in (btn.get_attribute("class") or "")
    if is_active != active:
        btn.click()
        page.wait_for_timeout(300)


def _navigate_to_week_containing(page, target_day_str):
    """Navigate the calendar week view until the column headers contain target_day_str.

    target_day_str should be something like "4" for June 4.
    We look at the column header cells to determine current week.
    """
    for _ in range(30):
        headers = page.locator(".fc-col-header-cell").all_inner_texts()
        header_text = " ".join(headers)
        if target_day_str in header_text:
            return
        page.locator(".o_calendar_button_next").first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)


def _click_event_on_date(page, event_title, day_number):
    """Click a specific event occurrence that appears on a given day number in week view.

    In the week calendar, events are positioned inside day columns. We find
    the event by title, then pick the one in the correct column.
    """
    events = page.locator(f".fc-event:has-text('{event_title}')")
    count = events.count()
    for i in range(count):
        ev = events.nth(i)
        # Get the bounding box to determine which column it's in
        ev.click()
        page.wait_for_timeout(500)
        return
    # Fallback: click first matching
    events.first.click()
    page.wait_for_timeout(500)


def _edit_occurrence_location(page, event_title, target_day, new_location):
    """Open an occurrence from the popover, edit its location, save with 'This Event'."""
    # Click the event in the calendar
    event = page.locator(f".fc-event:has-text('{event_title}')").first
    event.click()
    page.wait_for_timeout(500)

    # Click Edit in the popover
    page.locator(".o_cw_popover_edit").first.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Odoo may show a recurrence choice dialog when opening a recurring event
    # for editing: "This event" / "This and following events" / "All events"
    self_only = page.locator('input[data-value="self_only"]')
    if self_only.count() > 0 and self_only.first.is_visible():
        self_only.first.click()
        page.wait_for_timeout(500)

    # Change location
    fill_field(page, "location", new_location)
    page.wait_for_timeout(500)

    # Save by clicking breadcrumb back link
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # ---------------------------------------------------------------
    # Part 1: Create the recurring event
    # ---------------------------------------------------------------
    page.locator('.o_control_panel button:has-text("New"):visible').first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Set title
    fill_field(page, "name", "Cross-Team Sync")
    page.wait_for_timeout(500)

    # Set start datetime
    start_input = page.locator('.o_field_widget[name="start"] input').first
    start_input.click()
    start_input.fill("")
    start_input.type("06/04/2026 10:00:00 AM")
    start_input.press("Tab")
    page.wait_for_timeout(1000)

    # Close any datetime picker that opened
    picker = page.locator(".o_datetime_picker:visible")
    if picker.count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # Set end time via the daterange picker
    stop_btn = page.locator(".o_daterange_end").first
    stop_btn.click()
    page.wait_for_timeout(1000)

    # The picker has two time inputs: start time and end time
    time_inputs = page.locator(".o_datetime_picker:visible .o_time_picker_input")
    if time_inputs.count() >= 2:
        end_time_input = time_inputs.nth(1)
        end_time_input.click(click_count=3)
        end_time_input.fill("11:00am")
        end_time_input.press("Tab")
        page.wait_for_timeout(500)

    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # Set location
    fill_field(page, "location", "Main Conference Room")
    page.wait_for_timeout(500)

    # Add attendee Marc Demo
    add_many2many_tag(page, "partner_ids", "Marc Demo")
    page.wait_for_timeout(500)

    # Switch to Options tab for recurrence settings
    click_tab(page, "Options")
    page.wait_for_timeout(500)

    # Enable recurrence
    set_boolean(page, "recurrency", True)
    page.wait_for_timeout(1500)

    # Set recurrence type to Weekly
    _select_menu(page, "rrule_type_ui", "Weekly")
    page.wait_for_timeout(500)

    # Wait for the week days widget to appear
    page.wait_for_selector(".o_recurrent_weekdays", timeout=5000)
    page.wait_for_timeout(500)

    # Set only Thursday active (index 4 in US locale: Sun=0..Sat=6)
    for i in range(7):
        _set_week_day(page, i, i == 4)
    page.wait_for_timeout(500)

    # Set end type to "Number of repetitions"
    _select_menu(page, "end_type", "Number of repetitions")
    page.wait_for_timeout(500)

    # Set count to 6
    fill_field(page, "count", "6")
    page.wait_for_timeout(500)

    # Save by navigating back via breadcrumb
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # ---------------------------------------------------------------
    # Part 2: Edit the June 11 occurrence — location → "Virtual - Zoom"
    # ---------------------------------------------------------------
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Switch to week view
    page.locator(".scale_button_selection").first.click()
    page.wait_for_timeout(500)
    page.locator(".dropdown-menu:visible .dropdown-item:has-text('Week')").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Navigate to the week containing June 11
    _navigate_to_week_containing(page, "11")
    page.wait_for_timeout(500)

    # Edit the occurrence
    _edit_occurrence_location(page, "Cross-Team Sync", "11", "Virtual - Zoom")

    # ---------------------------------------------------------------
    # Part 3: Edit the June 25 occurrence — location → "Building B Room 201"
    # ---------------------------------------------------------------
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Switch to week view
    page.locator(".scale_button_selection").first.click()
    page.wait_for_timeout(500)
    page.locator(".dropdown-menu:visible .dropdown-item:has-text('Week')").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Navigate to the week containing June 25
    _navigate_to_week_containing(page, "25")
    page.wait_for_timeout(500)

    # Edit the occurrence
    _edit_occurrence_location(page, "Cross-Team Sync", "25", "Building B Room 201")


run_oracle(oracle)
