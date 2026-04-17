"""Oracle for event.register_attendee_confirm_check_in.

Open event, click Attendees stat, create new registration, confirm and
check in.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_stat_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Clear filters, switch to list.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)

    click_list_row(page, "Product Update Q2")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Click Attendees stat button.
    try:
        click_stat_button(page, "Attendees")
    except Exception:
        stat = page.locator("button.oe_stat_button:has-text('Attendees'):visible")
        if stat.count() > 0:
            stat.first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # New.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    new_btn.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    fill_field(page, "name", "Sofia Reyes")
    fill_field(page, "email", "sofia.reyes@partner.example")
    fill_field(page, "phone", "+44 20 7946 0312")

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Confirm.
    confirm_btn = page.locator(
        ".o_form_statusbar button[name='action_confirm']:visible, "
        ".o_form_statusbar button:has-text('Confirm'):visible"
    )
    if confirm_btn.count() > 0:
        confirm_btn.first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Check-in / Attended.
    attend_btn = page.locator(
        ".o_form_statusbar button[name='action_set_done']:visible, "
        ".o_form_statusbar button:has-text('Attended'):visible, "
        ".o_form_statusbar button:has-text('Check in'):visible"
    )
    attend_btn.first.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
