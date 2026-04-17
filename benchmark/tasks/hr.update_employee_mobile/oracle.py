"""Oracle for hr.update_employee_mobile."""

from benchmark.oracle_helpers import (
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
    fill_field,
    save_form,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    ensure_list_view(page)
    click_list_row(page, "Amelia Stone")
    _wait_for_ready(page)

    # Prefer a direct input field fill for mobile_phone
    try:
        fill_field(page, "mobile_phone", "+1 555 0472")
    except Exception:
        page.locator(
            ".o_field_widget[name='mobile_phone'] input, input[name='mobile_phone']"
        ).first.fill("+1 555 0472")
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
