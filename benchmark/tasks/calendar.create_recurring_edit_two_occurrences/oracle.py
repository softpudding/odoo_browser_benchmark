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
    full_url,
    login,
    navigate,
    run_oracle,
    set_boolean,
    save_form,
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
        btn = widget.locator("button, .dropdown-toggle, .o_select_menu_toggler")
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


def _navigate_to_month_containing(page, month_name):
    """Navigate the calendar month view until the header contains the month name (e.g. 'June')."""
    for _ in range(30):
        title = page.locator(".o_calendar_header h5").first.inner_text()
        if month_name.lower() in title.lower():
            return
        page.locator(".o_calendar_button_next").first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)


def _edit_occurrence_location(page, event_title, new_location):
    """Open an occurrence from the popover, edit its location, save with 'This Event'."""
    # Click the event in the calendar
    event = page.locator(f".fc-event:has-text('{event_title}')").first
    event.click()
    page.wait_for_timeout(800)

    # Click Edit in the popover
    edit_btn = page.locator(".o_cw_popover_edit, .o_cw_popover .o_cw_popover_edit")
    edit_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # In Odoo 19, the calendar form has inline radio buttons for
    # recurrence_update: self_only / future_events / all_events.
    # Select "This event" (self_only) before making changes.
    self_only = page.locator('input[data-value="self_only"]')
    if self_only.count() > 0 and self_only.first.is_visible():
        self_only.first.click()
        page.wait_for_timeout(500)

    # Change location
    fill_field(page, "location", new_location)
    page.wait_for_timeout(500)

    # Save by navigating back via breadcrumb (calendar form auto-saves)
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def oracle(page):
    login(page)

    # Navigate directly to the calendar event form view (new record)
    page.goto(full_url("/odoo/calendar/new"), timeout=120000)
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)
    _wait_for_ready(page)

    # ---------------------------------------------------------------
    # Part 1: Create the recurring event in the full form
    # ---------------------------------------------------------------
    # Wait for the form to load
    page.wait_for_selector(".o_form_view", timeout=30000)
    page.wait_for_timeout(1000)

    # Set title first (without Tab to avoid changing focus of other fields)
    name_inp = page.locator('.o_field_widget[name="name"] input').first
    name_inp.click()
    name_inp.fill("Cross-Team Sync")
    page.wait_for_timeout(300)

    # Set start datetime using the daterange widget + datetime picker.
    # Click the start element to activate it and open the picker.
    start_widget = page.locator('.o_field_widget[name="start"]').first
    start_el = start_widget.locator('[data-field="start"]').first
    start_el.click(force=True)
    page.wait_for_timeout(1000)

    # The datetime picker should now be open
    picker = page.locator(".o_datetime_picker:visible").first

    # Set the time FIRST using the time picker
    time_inputs = picker.locator(".o_time_picker_input")
    if time_inputs.count() > 0:
        # Click the start time input
        time_inputs.first.click()
        page.wait_for_timeout(300)
        # Clear and type the time value
        time_inputs.first.fill("10:00 AM")
        page.wait_for_timeout(300)
        # Use evaluate to dispatch input event
        time_inputs.first.evaluate("""el => {
            el.value = '10:00 AM';
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }""")
        page.wait_for_timeout(500)

    # Navigate to June 2026 in the picker
    for _ in range(20):
        header_parts = picker.locator(".o_datetime_picker_header .o_header_part")
        header_text = " ".join([h.inner_text() for h in header_parts.all()])
        if "Jun" in header_text and "2026" in header_text:
            break
        picker.locator(".o_datetime_picker_header .o_next").first.click()
        page.wait_for_timeout(300)

    # Click on day 4 (this commits the date with the already-set time)
    day_cells = picker.locator(".o_date_item_cell")
    for i in range(day_cells.count()):
        cell = day_cells.nth(i)
        cls = cell.get_attribute("class") or ""
        if cell.inner_text().strip() == "4" and "o_out_of_range" not in cls:
            cell.click()
            page.wait_for_timeout(500)
            break

    # Close the datetime picker
    for _ in range(5):
        if page.locator(".o_datetime_picker:visible").count() > 0:
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
        else:
            break

    # Click on the name field to move focus away
    name_inp.click(force=True)
    page.wait_for_timeout(800)

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
    # Part 2: Edit the June 11 occurrence — location -> "Virtual - Zoom"
    # ---------------------------------------------------------------
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Switch to month view for reliable navigation
    page.locator(".scale_button_selection").first.click()
    page.wait_for_timeout(500)
    page.locator(".dropdown-menu:visible .dropdown-item:has-text('Month')").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Navigate to June 2026
    _navigate_to_month_containing(page, "June")
    page.wait_for_timeout(500)

    # Find the Cross-Team Sync event on June 11
    # In month view, events are shown as blocks. We need to click the right one.
    # Find all Cross-Team Sync events and click the one in the June 11 cell.
    events = page.locator(".fc-event:has-text('Cross-Team Sync')")
    clicked = False
    for i in range(events.count()):
        ev = events.nth(i)
        # Check if this event is in the June 11 date cell
        # Get the parent day cell and check its date
        parent_cell = ev.locator("xpath=ancestor::td[@data-date]").first
        if parent_cell.count() > 0:
            date_attr = parent_cell.get_attribute("data-date")
            if date_attr and "2026-06-11" in date_attr:
                ev.click()
                clicked = True
                break

    if not clicked:
        # Fallback: try clicking by position - find the second occurrence
        events = page.locator(".fc-event:has-text('Cross-Team Sync')")
        if events.count() >= 2:
            events.nth(1).click()  # Second occurrence = June 11
        else:
            events.first.click()
    page.wait_for_timeout(800)

    # Click Edit in the popover
    edit_btn = page.locator(".o_cw_popover_edit")
    edit_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Select "This event" for recurrence update
    self_only = page.locator('input[data-value="self_only"]')
    if self_only.count() > 0 and self_only.first.is_visible():
        self_only.first.click()
        page.wait_for_timeout(500)

    # Change location
    fill_field(page, "location", "Virtual - Zoom")
    page.wait_for_timeout(500)

    # Save by navigating back
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # ---------------------------------------------------------------
    # Part 3: Edit the June 25 occurrence — location -> "Building B Room 201"
    # ---------------------------------------------------------------
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Switch to month view
    page.locator(".scale_button_selection").first.click()
    page.wait_for_timeout(500)
    page.locator(".dropdown-menu:visible .dropdown-item:has-text('Month')").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Navigate to June 2026
    _navigate_to_month_containing(page, "June")
    page.wait_for_timeout(500)

    # Find the Cross-Team Sync event on June 25
    events = page.locator(".fc-event:has-text('Cross-Team Sync')")
    clicked = False
    for i in range(events.count()):
        ev = events.nth(i)
        parent_cell = ev.locator("xpath=ancestor::td[@data-date]").first
        if parent_cell.count() > 0:
            date_attr = parent_cell.get_attribute("data-date")
            if date_attr and "2026-06-25" in date_attr:
                ev.click()
                clicked = True
                break

    if not clicked:
        # Fallback: try the 4th occurrence (Jun 4, 11, 18, 25)
        events = page.locator(".fc-event:has-text('Cross-Team Sync')")
        if events.count() >= 4:
            events.nth(3).click()
        else:
            events.last.click()
    page.wait_for_timeout(800)

    # Click Edit in the popover
    edit_btn = page.locator(".o_cw_popover_edit")
    edit_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Select "This event"
    self_only = page.locator('input[data-value="self_only"]')
    if self_only.count() > 0 and self_only.first.is_visible():
        self_only.first.click()
        page.wait_for_timeout(500)

    # Change location
    fill_field(page, "location", "Building B Room 201")
    page.wait_for_timeout(500)

    # Save by navigating back
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
