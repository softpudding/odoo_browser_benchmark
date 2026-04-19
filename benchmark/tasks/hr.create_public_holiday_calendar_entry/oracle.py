"""Oracle for hr.create_public_holiday_calendar_entry.

Navigate to Time Off > Configuration > Public Holidays (editable-bottom list),
click New to open a blank inline row, fill:
  - Name (plain char input)
  - Start Date (click daterange-start button -> type in exposed input -> Tab)
  - End Date (type in input that the daterange widget now exposes)
Leave Working Hours at default (empty == "All Schedules"), then Save.

Odoo 19 quirks encoded here:
  * The date_from / date_to cells use the `daterange` widget: initially
    each cell shows a <button data-field="date_{from,to}">. After the
    first button is clicked, BOTH get replaced with <input> elements and
    a datetime picker pops open.
  * Pressing Escape on an inline list row DISCARDS the row (loses all
    edits). We use Tab to advance focus and a click on the breadcrumb
    to close the picker without discarding the row.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


HOLIDAY_NAME = "Bench Founder Day"
DATE_FROM = "06/01/2026 00:00:00"
DATE_TO = "06/01/2026 23:59:59"


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-hr_holidays.open_view_public_holiday")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)
    _wait_for_ready(page)

    # Click "New" to open a blank inline row at the bottom.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)
    page.wait_for_selector(".o_data_row.o_selected_row", timeout=10000)

    # 1. Name -- standard char input in the row.
    row = page.locator(".o_data_row.o_selected_row").first
    name_input = row.locator("td[name='name'] input").first
    name_input.click()
    name_input.fill(HOLIDAY_NAME)
    page.wait_for_timeout(300)

    # 2. Start date -- click the daterange-start button, type, Tab.
    df_btn = page.locator("button[data-field='date_from']").first
    df_btn.click()
    page.wait_for_timeout(600)
    df_input = page.locator("input[data-field='date_from']").first
    df_input.click(click_count=3)
    df_input.fill("")
    df_input.type(DATE_FROM, delay=10)
    page.wait_for_timeout(300)
    df_input.press("Tab")
    page.wait_for_timeout(500)

    # 3. End date -- after Tab, date_to is exposed as <input>. The
    #    picker is still open but that's fine; we just need to type.
    dt_input = page.locator("input[data-field='date_to']").first
    dt_input.click(click_count=3)
    dt_input.fill("")
    dt_input.type(DATE_TO, delay=10)
    page.wait_for_timeout(300)
    dt_input.press("Tab")
    page.wait_for_timeout(500)

    # Close the picker popover without discarding the row (Escape
    # discards on inline lists). Clicking the breadcrumb is a safe
    # out-of-row target that commits the pending edits.
    try:
        page.locator(
            ".o_breadcrumb, .o_control_panel_breadcrumbs"
        ).first.click(position={"x": 5, "y": 5})
    except Exception:
        pass
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # Save the list (commit the pending row).
    save_btn = page.locator(
        ".o_list_button_save:visible, "
        ".o_list_record_save:visible, "
        ".o_form_button_save:visible, "
        ".o_control_panel button[name='save']:visible, "
        ".o_control_panel_main_buttons button:has-text('Save'):visible"
    )
    if save_btn.count() > 0:
        save_btn.first.click()
        page.wait_for_timeout(1500)
    _wait_no_loading(page)
    page.wait_for_timeout(800)


run_oracle(oracle)
