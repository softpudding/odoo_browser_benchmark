"""Oracle for calendar.schedule_recurring_steering_sync.

Create a new recurring meeting "Northwind Steering Sync" on May 7 2026
14:30-15:15, weekly on Thursday for 3 occurrences. Invite Avery Stone,
set location and description. Then edit the 2nd occurrence (May 14) to
change location to "War Room C", choosing "This Event".
"""

from benchmark.oracle_helpers import (
    fill_field,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_boolean,
    set_many2one,
    add_many2many_tag,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Click New to create a new event
    page.locator(".o_control_panel button:has-text('New'):visible").first.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Set the title
    fill_field(page, "name", "Northwind Steering Sync")
    page.wait_for_timeout(500)

    # Set start datetime: 05/07/2026 14:30:00
    # Odoo 19 datetime fields use button-based pickers. Use JS to set the value
    # directly via the OWL component, then trigger the field's onchange.
    page.evaluate("""() => {
        // Find the start datetime field widget and set its value
        const startWidget = document.querySelector('.o_field_widget[name="start"]');
        const startInput = startWidget && startWidget.querySelector('input');
        if (startInput) {
            // If there's an input, use it directly
            startInput.value = '';
            startInput.dispatchEvent(new Event('input', { bubbles: true }));
            startInput.value = '05/07/2026 14:30:00';
            startInput.dispatchEvent(new Event('input', { bubbles: true }));
            startInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""")
    # Fallback: try clicking and typing into the field
    start_widget = page.locator(".o_field_widget[name='start']").first
    start_input = start_widget.locator("input")
    if start_input.count() > 0 and start_input.first.is_visible():
        start_input.first.click()
        start_input.first.fill("")
        start_input.first.type("05/07/2026 14:30:00")
        start_input.first.press("Tab")
    else:
        # Button-based picker: click to open, then navigate
        start_btn = start_widget.locator("button, .o_input, .o_datetime_button").first
        start_btn.click()
        page.wait_for_timeout(500)
        # Type the date directly if a text input appeared in the picker
        picker_input = page.locator(".o_datetime_picker input:visible")
        if picker_input.count() > 0:
            picker_input.first.fill("05/07/2026 14:30:00")
            picker_input.first.press("Enter")
        page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # Set stop datetime: 05/07/2026 15:15:00
    stop_widget = page.locator(".o_field_widget[name='stop']").first
    stop_input = stop_widget.locator("input")
    if stop_input.count() > 0 and stop_input.first.is_visible():
        stop_input.first.click()
        stop_input.first.fill("")
        stop_input.first.type("05/07/2026 15:15:00")
        stop_input.first.press("Tab")
    else:
        stop_btn = stop_widget.locator("button, .o_input, .o_datetime_button").first
        stop_btn.click()
        page.wait_for_timeout(500)
        picker_input = page.locator(".o_datetime_picker input:visible")
        if picker_input.count() > 0:
            picker_input.first.fill("05/07/2026 15:15:00")
            picker_input.first.press("Enter")
        page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # Add attendee Avery Stone (partner_ids is many2many)
    add_many2many_tag(page, "partner_ids", "Avery Stone")
    page.wait_for_timeout(500)

    # Set location
    fill_field(page, "location", "War Room B")
    page.wait_for_timeout(500)

    # Set description - try textarea first, then HTML editor
    desc_widget = page.locator(".o_field_widget[name='description']").first
    desc_textarea = desc_widget.locator("textarea")
    desc_editable = desc_widget.locator(".note-editable, .odoo-editor-editable, .o_wysiwyg_wrapper [contenteditable='true']")
    if desc_textarea.count() > 0 and desc_textarea.first.is_visible():
        desc_textarea.first.click()
        desc_textarea.first.fill("Escalate blockers before launch freeze.")
    elif desc_editable.count() > 0:
        desc_editable.first.click()
        desc_editable.first.fill("Escalate blockers before launch freeze.")
    else:
        # Try clicking the widget itself and typing
        desc_widget.click()
        page.keyboard.type("Escalate blockers before launch freeze.")
    page.wait_for_timeout(500)

    # Enable recurrence
    set_boolean(page, "recurrency", True)
    page.wait_for_timeout(500)

    # Set recurrence to weekly
    page.locator(".o_field_widget[name='rrule_type'] select").select_option(label="Weekly")
    page.wait_for_timeout(300)

    # Ensure Thursday is selected
    thu_cb = page.locator(".o_field_widget[name='thu'] input[type='checkbox']").first
    if not thu_cb.is_checked():
        thu_cb.click()
    page.wait_for_timeout(300)

    # Uncheck other days if checked
    for day in ["mon", "tue", "wed", "fri", "sat", "sun"]:
        cb = page.locator(f".o_field_widget[name='{day}'] input[type='checkbox']")
        if cb.count() > 0 and cb.first.is_checked():
            cb.first.click()
            page.wait_for_timeout(200)

    # Set end type to "Number of repetitions" and count to 3
    page.locator(".o_field_widget[name='end_type'] select").select_option(label="Number of repetitions")
    page.wait_for_timeout(300)

    fill_field(page, "count", "3")
    page.wait_for_timeout(500)

    # Save the event
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Now navigate to week of May 14 to edit the 2nd occurrence
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Switch to week view via scale dropdown
    page.locator(".scale_button_selection").first.click()
    page.wait_for_timeout(500)
    page.locator(".dropdown-menu:visible .dropdown-item:has-text('Week')").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Navigate to the week containing May 14, 2026
    for _ in range(30):
        headers = page.locator(".fc-col-header-cell").all_inner_texts()
        header_text = " ".join(headers)
        if "14" in header_text:
            break
        page.locator(".o_calendar_button_next").first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    page.wait_for_timeout(500)

    # Click the "Northwind Steering Sync" event on May 14
    event = page.locator(".fc-event:has-text('Northwind Steering Sync')").first
    event.click()
    page.wait_for_timeout(500)

    # Click Edit
    page.locator(".o_cw_popover button:has-text('Edit')").first.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Change location to "War Room C"
    fill_field(page, "location", "War Room C")
    page.wait_for_timeout(500)

    # Save
    save_form(page)
    page.wait_for_timeout(1000)

    # Recurrence dialog — choose "This Event"
    modal = page.locator(".modal:visible").last
    modal.locator("input[value='self']").first.click()
    page.wait_for_timeout(300)

    modal.locator("button.btn-primary").first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


run_oracle(oracle)
