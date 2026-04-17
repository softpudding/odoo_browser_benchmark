"""Oracle for purchase.update_rfq_deadline."""

from benchmark.oracle_helpers import (
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    ensure_list_view(page)
    click_list_row(page, "BENCH-RFQ-DEADLINE-01")
    _wait_for_ready(page)
    edit_btn = page.locator(
        ".o_control_panel button:has-text('Edit'):visible, button.o_form_button_edit:visible"
    )
    if edit_btn.count() > 0:
        edit_btn.first.click()
        page.wait_for_timeout(600)
        _wait_no_loading(page)
    widget = page.locator(".o_field_widget[name='date_order']").first
    toggle = widget.locator("button:visible, .o_input:visible, input:visible").first
    toggle.click()
    page.wait_for_timeout(600)

    for _ in range(12):
        header = page.locator(".o_datetime_picker .o_header_part:visible").first
        if "May 2026" in header.inner_text():
            break
        page.locator(".o_datetime_picker .o_next:visible").first.click()
        page.wait_for_timeout(200)

    cell_20 = page.locator(
        ".o_datetime_picker .o_date_item_cell:visible:not(.o_out_of_range)"
    ).filter(has_text="20")
    cell_20.first.click()
    page.wait_for_timeout(300)
    apply_btn = page.locator(".o_datetime_picker .o_apply:visible")
    if apply_btn.count() > 0:
        apply_btn.first.click()
        page.wait_for_timeout(300)
    page.wait_for_timeout(300)
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
