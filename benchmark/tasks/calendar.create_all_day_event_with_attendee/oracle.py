"""Oracle for calendar.create_all_day_event_with_attendee."""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def _set_all_day_date(page, target_month: str, target_day: str) -> None:
    page.locator(
        ".o_field_widget[name='start_date'] button.o_daterange_start"
    ).first.click()
    page.wait_for_timeout(500)
    for _ in range(12):
        header = page.locator(
            ".o_datetime_picker .o_header_part:visible, "
            ".o_date_picker .o_header_part:visible"
        ).first
        if target_month in header.inner_text():
            break
        page.locator(
            ".o_datetime_picker .o_next:visible, "
            ".o_date_picker .o_next:visible"
        ).first.click()
        page.wait_for_timeout(250)

    page.locator(
        ".o_datetime_picker .o_date_item_cell:visible:not(.o_out_of_range), "
        ".o_date_picker .o_date_item_cell:visible:not(.o_out_of_range)"
    ).filter(has_text=target_day).first.click()
    page.wait_for_timeout(400)
    apply_btn = page.locator(
        ".o_datetime_picker .o_apply:visible, .o_date_picker .o_apply:visible"
    )
    if apply_btn.count() > 0:
        apply_btn.first.click()
        page.wait_for_timeout(300)
    if page.locator(".o_datetime_picker:visible, .o_date_picker:visible").count() > 0:
        page.press("body", "Escape")
        page.wait_for_timeout(300)


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    _wait_no_loading(page)

    page.locator('.o_control_panel button:has-text("New"):visible').first.click()
    page.wait_for_timeout(1200)

    edit_btn = page.locator(
        ".modal:visible button:has-text('Edit'), .popover:visible button:has-text('Edit')"
    )
    if edit_btn.count() > 0:
        edit_btn.first.click()
        page.wait_for_timeout(1000)

    _wait_for_ready(page)

    name_input = page.locator(".o_field_widget[name='name'] input:visible").first
    name_input.fill("")
    name_input.type("Operations Offsite")
    name_input.press("Tab")
    page.wait_for_timeout(300)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    page.locator(
        ".o_field_widget[name='allday'] .o_boolean_toggle"
    ).first.click(force=True)
    page.wait_for_timeout(800)
    _set_all_day_date(page, "June 2026", "18")
    page.wait_for_timeout(600)

    location_input = page.locator(
        ".o_field_widget[name='location'] input:visible"
    ).first
    location_input.fill("")
    location_input.type("Mountain View Campus")
    location_input.press("Tab")
    page.wait_for_timeout(300)
    attendee_input = page.locator(
        ".o_field_widget[name='partner_ids'] input:visible"
    ).first
    attendee_input.click()
    attendee_input.fill("Marc Demo")
    page.wait_for_timeout(800)
    page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item:not(.o_m2o_dropdown_option) a, "
        ".dropdown-menu:visible .o-autocomplete--dropdown-item:not(.o_m2o_dropdown_option) a"
    ).first.click(force=True)
    page.wait_for_timeout(400)
    admin_tag = page.locator(
        ".o_field_widget[name='partner_ids'] .o_tag:has-text('Administrator') .o_delete, "
        ".o_field_widget[name='partner_ids'] [aria-label='Administrator'] .o_delete"
    )
    if admin_tag.count() > 0:
        admin_tag.first.click()
        page.wait_for_timeout(300)

    page.locator(".o_notebook .nav-link:has-text('Options')").first.click()
    page.wait_for_timeout(500)
    desc_editable = page.locator(
        '.o_field_widget[name="description"] .note-editable, '
        '.o_field_widget[name="description"] .odoo-editor-editable, '
        '.o_field_widget[name="description"] [contenteditable="true"]'
    ).first
    desc_editable.click()
    desc_editable.press("Control+A")
    page.keyboard.type("Annual planning offsite for operations leads.")
    page.wait_for_timeout(400)

    page.locator(".o_breadcrumb a").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
