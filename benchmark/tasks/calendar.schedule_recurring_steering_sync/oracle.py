"""Oracle for calendar.schedule_recurring_steering_sync.

Create a new recurring meeting "Northwind Steering Sync" on May 7 2026
14:30-15:15, weekly on Thursday for 3 occurrences. Invite Avery Stone,
set location and description. Then edit the 2nd occurrence (May 14) to
change location to "War Room C", choosing "This Event".
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
        # Check if already showing the right value
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

    day_index: 0-based, starting from the locale's week start.
    For US locale (weekStart=0/Sunday): 0=Sun,1=Mon,2=Tue,3=Wed,4=Thu,5=Fri,6=Sat
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

    # ---------------------------------------------------------------
    # Part 1: Create the recurring event
    # ---------------------------------------------------------------
    page.locator('.o_control_panel button:has-text("New"):visible').first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # Set title
    fill_field(page, "name", "Northwind Steering Sync")
    page.wait_for_timeout(500)

    # Set start datetime -- for a new event the start field renders as <input>
    start_input = page.locator('.o_field_widget[name="start"] input').first
    start_input.click()
    start_input.fill("")
    start_input.type("05/07/2026 02:30:00 PM")
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
        end_time_input.fill("3:15pm")
        end_time_input.press("Tab")
        page.wait_for_timeout(500)

    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # Add attendee Avery Stone
    add_many2many_tag(page, "partner_ids", "Avery Stone")
    page.wait_for_timeout(500)

    # Set location
    fill_field(page, "location", "War Room B")
    page.wait_for_timeout(500)

    # Switch to Options tab
    click_tab(page, "Options")
    page.wait_for_timeout(500)

    # Set description (HTML contenteditable field)
    desc_editable = page.locator(
        '.o_field_widget[name="description"] .note-editable, '
        '.o_field_widget[name="description"] .odoo-editor-editable, '
        '.o_field_widget[name="description"] [contenteditable="true"]'
    ).first
    desc_editable.click()
    page.keyboard.type("Escalate blockers before launch freeze.")
    page.wait_for_timeout(500)

    # Enable recurrence
    set_boolean(page, "recurrency", True)
    page.wait_for_timeout(1500)

    # The default recurrence type is "Weekly" -- verify and set if needed
    _select_menu(page, "rrule_type_ui", "Weekly")
    page.wait_for_timeout(500)

    # Set the day of week using the calendar_week_days widget.
    # The widget shows round buttons for each day. Order depends on locale.
    # For the default US locale: Sun(0), Mon(1), Tue(2), Wed(3), Thu(4), Fri(5), Sat(6)
    # We need Thursday active and all others inactive.
    # The current day is Wed (today is Apr 15 2026, a Wednesday), so
    # Wed might be pre-selected. Let me deactivate all except Thu.

    # Wait for the week days widget to appear
    page.wait_for_selector(".o_recurrent_weekdays", timeout=5000)
    page.wait_for_timeout(500)

    # Deactivate all days except Thursday (index 4)
    for i in range(7):
        if i == 4:  # Thursday
            _set_week_day(page, i, True)
        else:
            _set_week_day(page, i, False)
    page.wait_for_timeout(500)

    # Set end type to "Number of repetitions"
    _select_menu(page, "end_type", "Number of repetitions")
    page.wait_for_timeout(500)

    # Set count to 3
    fill_field(page, "count", "3")
    page.wait_for_timeout(500)

    # Save by navigating back via breadcrumb
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # ---------------------------------------------------------------
    # Part 2: Edit the 2nd occurrence (May 14) location
    # ---------------------------------------------------------------
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Switch to week view
    page.locator(".scale_button_selection").first.click()
    page.wait_for_timeout(500)
    page.locator(".dropdown-menu:visible .dropdown-item:has-text('Week')").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Navigate to the week of May 14, 2026
    for _ in range(30):
        events = page.locator(".fc-event:has-text('Northwind Steering Sync')")
        if events.count() > 0:
            headers = page.locator(".fc-col-header-cell").all_inner_texts()
            header_text = " ".join(headers)
            if "14" in header_text:
                break
        page.locator(".o_calendar_button_next").first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    page.wait_for_timeout(500)

    # Click the event on May 14
    event = page.locator(".fc-event:has-text('Northwind Steering Sync')").first
    event.click()
    page.wait_for_timeout(500)

    # Click Edit
    page.locator(".o_cw_popover_edit").first.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Select "This event" radio
    page.locator('input[data-value="self_only"]').first.click()
    page.wait_for_timeout(500)

    # Change location
    fill_field(page, "location", "War Room C")
    page.wait_for_timeout(500)

    # Save by navigating back via breadcrumb
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
