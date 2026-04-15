"""Oracle for calendar.edit_single_recurrence_occurrence.

Navigate to Calendar week view for Apr 27 2026, click the "Ops Standup"
occurrence, change Location from "Main Office" to "Building B Room 4",
choose "This Event" in the recurrence dialog, and save.
"""

from benchmark.oracle_helpers import (
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
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

    # Navigate forward until we reach the week containing Apr 27, 2026
    for _ in range(30):
        headers = page.locator(".fc-col-header-cell").all_inner_texts()
        header_text = " ".join(headers)
        if "27" in header_text:
            break
        page.locator(".o_calendar_button_next").first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    page.wait_for_timeout(500)

    # Click the "Ops Standup" event on Apr 27
    event = page.locator(".fc-event:has-text('Ops Standup')").first
    event.click()
    page.wait_for_timeout(500)

    # A popover appears — click Edit to open the form
    page.locator(".o_cw_popover button:has-text('Edit')").first.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Change location
    fill_field(page, "location", "Building B Room 4")
    page.wait_for_timeout(500)

    # Save the form
    save_form(page)
    page.wait_for_timeout(1000)

    # Recurrence dialog appears — choose "This Event"
    modal = page.locator(".modal:visible").last
    modal.locator("input[value='self']").first.click()
    page.wait_for_timeout(300)

    # Confirm
    modal.locator("button.btn-primary").first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


run_oracle(oracle)
