"""Oracle for hr.add_resume_line_update_mobile."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    click_list_row(page, "Marina Ortega")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    edit_btn = page.locator(
        ".o_control_panel button:has-text('Edit'):visible, "
        "button.o_form_button_edit:visible"
    )
    if edit_btn.count() > 0:
        edit_btn.first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)

    set_many2one(page, "work_location_id", "Home")
    page.wait_for_timeout(400)

    click_tab(page, "Resume")
    page.wait_for_timeout(800)

    page.get_by_role("button", name="Create Resume Lines").click()
    page.wait_for_timeout(1000)

    modal = page.locator(".modal:visible").last
    if modal.count() > 0:
        badge = modal.locator(
            ".o_field_widget[name='line_type_id'] .o_selection_badge:has-text('Certification')"
        )
        if badge.count() > 0:
            badge.first.click()
            page.wait_for_timeout(400)

        title_input = modal.locator(".o_field_widget[name='name'] input").first
        title_input.click()
        title_input.fill("ISO 27001 Internal Auditor")
        title_input.press("Tab")
        page.wait_for_timeout(300)

        start_input = modal.locator(".o_field_widget[name='date_start'] input").first
        start_input.click()
        start_input.fill("05/01/2026")
        start_input.press("Tab")
        page.wait_for_timeout(300)

        end_input = modal.locator(".o_field_widget[name='date_end'] input").first
        end_input.click()
        end_input.fill("05/01/2027")
        end_input.press("Tab")
        page.wait_for_timeout(300)

        modal.locator(
            ".modal-footer button.o_form_button_save, .modal-footer button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1200)
        _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
