"""Oracle for calendar.make_single_occurrence_all_day.

Navigate to Calendar week containing May 19 2026, click the "Warehouse
Walkthrough" occurrence on May 19, turn on All Day, change Location to
"Remote Review Hub", choose "This Event" in recurrence dialog.
"""

from benchmark.oracle_helpers import (
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
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

    # Navigate forward until we reach the week containing May 19, 2026
    for _ in range(30):
        headers = page.locator(".fc-col-header-cell").all_inner_texts()
        header_text = " ".join(headers)
        if "19" in header_text:
            break
        page.locator(".o_calendar_button_next").first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    page.wait_for_timeout(500)

    # Click the "Warehouse Walkthrough" event on May 19
    event = page.locator(".fc-event:has-text('Warehouse Walkthrough')").first
    event.click()
    page.wait_for_timeout(500)

    # Click Edit in the popover
    page.locator(".o_cw_popover button:has-text('Edit')").first.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Turn on All Day
    set_boolean(page, "allday", True)
    page.wait_for_timeout(500)

    # Change location
    fill_field(page, "location", "Remote Review Hub")
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
