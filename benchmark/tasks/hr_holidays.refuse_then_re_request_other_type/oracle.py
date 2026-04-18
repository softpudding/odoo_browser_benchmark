"""Oracle for hr_holidays.refuse_then_re_request_other_type."""

from benchmark.oracle_helpers import (
    click_list_row,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    set_many2one,
    _wait_no_loading,
)


REASON_TEXT = "Use sick leave instead"


def _fill_daterange(page, field, value):
    """Click the button representation, then fill the revealed input."""
    target = page.locator(f"[data-field='{field}']")
    target.first.click()
    page.wait_for_timeout(400)
    inp = page.locator(f"input[data-field='{field}']")
    inp.first.fill("")
    inp.first.type(value)
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)


def _clear_facets(page):
    for _ in range(6):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(400)
        except Exception:
            break
    _wait_no_loading(page)


def _switch_to_list(page):
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)


def oracle(page):
    login(page)

    # ------------------------------------------------------------------
    # Step A: refuse the existing Paid Time Off request.
    # ------------------------------------------------------------------
    navigate(page, "/odoo/time-off-approval")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    _switch_to_list(page)
    _clear_facets(page)
    page.wait_for_timeout(500)

    click_list_row(page, "Family vacation")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    refuse_btn = page.locator(
        ".o_form_statusbar button[name='action_refuse']:visible"
    )
    if refuse_btn.count() > 0:
        refuse_btn.first.click()
    else:
        page.locator("button[name='action_refuse']:visible").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # ------------------------------------------------------------------
    # Step B: post the refusal reason to the chatter on the refused leave.
    # ------------------------------------------------------------------
    chatter = page.locator(".o-mail-Chatter, .o_chatter")
    if chatter.count() > 0:
        chatter.first.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

    send_msg_btn = page.locator(
        "button:has-text('Send message'), "
        ".o-mail-Chatter button:has-text('Send message'), "
        ".o_Chatter button:has-text('Send message')"
    ).first
    send_msg_btn.click()
    page.wait_for_timeout(800)

    composer = page.locator(
        ".o-mail-Composer .o-mail-Composer-input, "
        ".o-mail-composer [contenteditable='true'], "
        "div[contenteditable='true'].odoo-editor-editable, "
        ".o-mail-Composer-input [contenteditable='true']"
    ).last
    composer.click()
    page.wait_for_timeout(300)
    composer.fill(REASON_TEXT)
    page.wait_for_timeout(300)

    send_btn = page.locator(
        "button.o-mail-Composer-send, "
        ".o-mail-Composer button:has-text('Send'), "
        ".o-mail-Composer button[type='submit']"
    ).first
    send_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # ------------------------------------------------------------------
    # Step C: go back to the approval list and create a fresh Sick Time
    # Off request for Eve Employee on the same dates.
    # ------------------------------------------------------------------
    navigate(page, "/odoo/time-off-approval")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)
    _switch_to_list(page)
    _clear_facets(page)

    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        "button.o-kanban-button-new:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    if new_btn.count() > 0:
        new_btn.first.click()
    else:
        page.locator("button:has-text('New'):visible").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Set employee to Eve Employee. The field may be named employee_id;
    # with the responsible group active, admin can edit it.
    set_many2one(page, "employee_id", "Eve Employee")
    page.wait_for_timeout(500)

    set_many2one(page, "holiday_status_id", "Sick Time Off")
    page.wait_for_timeout(500)

    _fill_daterange(page, "request_date_from", "08/10/2026")
    _fill_daterange(page, "request_date_to", "08/12/2026")

    fill_text_field(page, "name", "Sick leave per manager")

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
