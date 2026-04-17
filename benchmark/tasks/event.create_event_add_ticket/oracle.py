"""Oracle for event.create_event_add_ticket.

Create event "Odoo Community Days 2026" with dates July 15-17, 2026,
add a "Standard Pass" ticket at 75.00 with 200 max attendees.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/events/new")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Set event name (text widget = textarea)
    name_widget = page.locator(".o_field_widget[name='name']").first
    textarea = name_widget.locator("textarea")
    if textarea.count() > 0 and textarea.first.is_visible():
        textarea.first.click()
        textarea.first.fill("Odoo Community Days 2026")
        textarea.first.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Set date_begin using the daterange widget
    # The widget has options={'end_date_field': 'date_end'}
    # It renders as a single span/div with two inputs inside
    date_widget = page.locator(".o_field_widget[name='date_begin']").first

    # Click on the widget to activate it
    date_widget.click()
    page.wait_for_timeout(500)

    # Find all inputs in the daterange widget
    inputs = date_widget.locator("input")
    visible_inputs = date_widget.locator("input:visible")

    if visible_inputs.count() >= 2:
        # Start date
        visible_inputs.nth(0).click(click_count=3)
        visible_inputs.nth(0).press("Control+a")
        visible_inputs.nth(0).type("07/15/2026 09:00:00")
        visible_inputs.nth(0).press("Tab")
        page.wait_for_timeout(500)

        # End date
        visible_inputs.nth(1).click(click_count=3)
        visible_inputs.nth(1).press("Control+a")
        visible_inputs.nth(1).type("07/17/2026 17:00:00")
        visible_inputs.nth(1).press("Tab")
        page.wait_for_timeout(500)
    elif visible_inputs.count() == 1:
        visible_inputs.first.click(click_count=3)
        visible_inputs.first.press("Control+a")
        visible_inputs.first.type("07/15/2026 09:00:00")
        visible_inputs.first.press("Tab")
        page.wait_for_timeout(1000)
        # Check for second input after tab
        vis2 = date_widget.locator("input:visible")
        if vis2.count() >= 2:
            vis2.nth(1).click(click_count=3)
            vis2.nth(1).press("Control+a")
            vis2.nth(1).type("07/17/2026 17:00:00")
            vis2.nth(1).press("Tab")
            page.wait_for_timeout(500)
    elif inputs.count() >= 1:
        # Inputs exist but aren't visible - try clicking to reveal
        first_input = inputs.first
        first_input.click(force=True)
        page.wait_for_timeout(500)
        first_input.fill("07/15/2026 09:00:00")
        first_input.press("Tab")
        page.wait_for_timeout(500)

    # Close datepicker
    try:
        page.press("body", "Escape")
    except Exception:
        pass
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Click the Registration tab to add tickets
    try:
        click_tab(page, "Registration")
    except Exception:
        pass
    page.wait_for_timeout(500)

    # Add a ticket line
    click_add_a_line(page)
    page.wait_for_timeout(500)

    # Set ticket details on the new row
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    row_idx = rows.count() - 1
    set_o2m_field(page, row_idx, "name", "Standard Pass")
    page.wait_for_timeout(300)
    set_o2m_field(page, row_idx, "price", "75")
    page.wait_for_timeout(300)
    set_o2m_field(page, row_idx, "seats_max", "200")
    page.wait_for_timeout(300)

    # Save the event
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
