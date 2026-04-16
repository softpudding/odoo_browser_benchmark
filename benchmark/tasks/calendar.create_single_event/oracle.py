"""Oracle for calendar.create_single_event.

Create a one-time calendar event "Q2 Strategy Review" on May 8, 2026,
2-4 PM, with location, description, and Marc Demo as attendee.
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_datetime,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Click New to create a new event
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    )
    if new_btn.count() > 0:
        new_btn.first.click()
    else:
        # In calendar view, click on a time slot or use the + button
        # Try clicking on the "New Event" or "New" button
        page.locator("button:has-text('New'):visible").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Check if a modal dialog opened (quick create) or a form view
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        # We're in a quick-create modal — fill basic fields and click Edit
        # or fill fields here
        name_input = modal.last.locator(
            ".o_field_widget[name='name'] input"
        )
        if name_input.count() > 0:
            name_input.first.fill("Q2 Strategy Review")
        # Look for "Edit" or "More Options" to open full form
        edit_btn = modal.last.locator(
            "button:has-text('Edit'), button:has-text('More'), "
            "a:has-text('Edit'), a:has-text('More')"
        )
        if edit_btn.count() > 0:
            edit_btn.first.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)

    # Now in the form view — set fields
    # Title
    fill_field(page, "name", "Q2 Strategy Review")
    page.wait_for_timeout(300)

    # Start datetime: May 8, 2026 14:00
    set_datetime(page, "start", "05/08/2026 14:00:00")
    page.wait_for_timeout(500)

    # End datetime: May 8, 2026 16:00
    set_datetime(page, "stop", "05/08/2026 16:00:00")
    page.wait_for_timeout(500)

    # Location
    fill_field(page, "location", "Conference Room A")
    page.wait_for_timeout(300)

    # Description
    desc_field = page.locator(
        ".o_field_widget[name='description'] .note-editable, "
        ".o_field_widget[name='description'] textarea, "
        ".o_field_widget[name='description'] .odoo-editor-editable"
    )
    if desc_field.count() > 0:
        desc_field.first.click()
        desc_field.first.fill(
            "Review Q2 objectives and align on priorities for the team."
        )
    page.wait_for_timeout(300)

    # Add Marc Demo as attendee
    add_many2many_tag(page, "partner_ids", "Marc Demo")
    page.wait_for_timeout(500)

    # Save
    save_form(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
