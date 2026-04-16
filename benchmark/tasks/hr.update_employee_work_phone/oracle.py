"""Oracle for hr.update_employee_work_phone."""

from benchmark.oracle_helpers import (
    fill_field,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    ensure_list_view,
    search_for,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    ensure_list_view(page)
    page.wait_for_timeout(500)

    search_for(page, "Sofia Chen")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    row = page.locator(".o_list_view .o_data_row").first
    row.click()
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    edit_btn = page.locator(
        "button.o_form_button_edit:visible, "
        ".o_control_panel button:has-text('Edit'):visible"
    )
    if edit_btn.count() > 0:
        edit_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    fill_field(page, "work_phone", "+1 555 0211")
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
