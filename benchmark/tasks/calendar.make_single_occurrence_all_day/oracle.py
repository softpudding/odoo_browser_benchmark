"""Oracle for calendar.make_single_occurrence_all_day.

Navigate to Calendar week containing May 19 2026, click the "Warehouse
Walkthrough" occurrence on May 19, turn on All Day, change Location to
"Remote Review Hub", choose "This Event" via recurrence_update radio.
"""

from benchmark.oracle_helpers import (
    fill_field,
    login,
    navigate,
    run_oracle,
    set_boolean,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    # Switch to week view via scale dropdown
    page.locator(".scale_button_selection").first.click()
    page.wait_for_timeout(500)
    page.locator(".dropdown-menu:visible .dropdown-item:has-text('Week')").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Navigate forward until we see the "Warehouse Walkthrough" event.
    # The event repeats on Tuesdays starting May 5, so the first occurrence
    # visible in week view will appear in the week of May 3-9.
    # We want the May 19 occurrence specifically.
    # Strategy: keep navigating until we see the event, then check if the
    # week contains the 19th. If not, advance to the next occurrence.
    found_target_week = False
    for _ in range(30):
        events = page.locator(".fc-event:has-text('Warehouse Walkthrough')")
        if events.count() > 0:
            # Check if this is the week containing the 19th
            headers = page.locator(".fc-col-header-cell").all_inner_texts()
            header_text = " ".join(headers)
            # The Tue column should show "19"
            if "19" in header_text:
                found_target_week = True
                break
        page.locator(".o_calendar_button_next").first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    page.wait_for_timeout(500)

    # Click the "Warehouse Walkthrough" event on May 19
    event = page.locator(".fc-event:has-text('Warehouse Walkthrough')").first
    event.click()
    page.wait_for_timeout(500)

    # Click Edit (it's an <a> link in Odoo 19)
    page.locator(".o_cw_popover_edit").first.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Select "This event" (self_only) via the inline radio
    page.locator('input[data-value="self_only"]').first.click()
    page.wait_for_timeout(500)

    # Turn on All Day
    set_boolean(page, "allday", True)
    page.wait_for_timeout(500)

    # Change location
    fill_field(page, "location", "Remote Review Hub")
    page.wait_for_timeout(500)

    # Save by navigating back via breadcrumb
    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
