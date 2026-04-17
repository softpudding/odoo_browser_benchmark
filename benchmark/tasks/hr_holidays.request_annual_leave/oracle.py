"""Oracle for hr_holidays.request_annual_leave."""

from benchmark.oracle_helpers import (
    fill_text_field,
    login,
    navigate,
    run_oracle,
    set_many2one,
    _wait_no_loading,
)


def _fill_daterange(page, field, value):
    """Fill a daterange sub-field identified by data-field attribute.

    Handles the button→input toggle by clicking the current representation,
    waiting for the input to be rendered, then typing.
    """
    # There may be either a button or an input with the given data-field
    target = page.locator(
        f"[data-field='{field}']"
    )
    target.first.click()
    page.wait_for_timeout(400)
    # After click, element should transition to <input>. Grab the input.
    inp = page.locator(f"input[data-field='{field}']")
    inp.first.fill("")
    inp.first.type(value)
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)


def oracle(page):
    login(page)
    navigate(page, "/odoo/time-off")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    new_btn = page.locator(
        "button.o_list_button_add:visible, button.o-kanban-button-new:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    if new_btn.count() > 0:
        new_btn.first.click()
    else:
        page.locator("button:has-text('New'):visible").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    set_many2one(page, "holiday_status_id", "Paid Time Off")

    _fill_daterange(page, "request_date_from", "07/20/2026")
    _fill_daterange(page, "request_date_to", "07/22/2026")

    fill_text_field(page, "name", "Family vacation to Iceland")

    save_btn = page.locator(
        "button.o_form_button_save:visible, "
        ".o_control_panel button[data-tooltip='Save']:visible"
    )
    if save_btn.count() > 0:
        save_btn.first.click()
    else:
        page.keyboard.press("Control+s")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
