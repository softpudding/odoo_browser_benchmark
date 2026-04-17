"""Oracle for account.partial_pay_vendor_bill_with_memo."""

from benchmark.oracle_helpers import (
    click_list_row,
    ensure_list_view,
    login,
    modal_click_button,
    modal_fill_field,
    modal_set_date,
    navigate,
    run_oracle,
    _dismiss_tooltips,
    _wait_no_loading,
    _wait_for_ready,
)


def _modal_fill_char(page, field_name: str, value: str) -> None:
    modal = page.locator(".modal:visible").last
    widget = modal.locator(f".o_field_widget[name='{field_name}']").first
    editor = widget.locator(
        "input:visible, textarea:visible, .odoo-editor-editable:visible, [contenteditable='true']:visible"
    ).first
    editor.click(force=True)
    tag_name = editor.evaluate("el => el.tagName.toLowerCase()")
    if tag_name in {"input", "textarea"}:
        editor.fill("")
        editor.fill(value)
        editor.press("Tab")
    else:
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(value)
        editor.press("Tab")
    page.wait_for_timeout(500)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/vendor-bills")
    _wait_no_loading(page)

    ensure_list_view(page)
    click_list_row(page, "VB-PARTIAL-01")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    _dismiss_tooltips(page)
    pay_btn = page.locator(
        ".o_statusbar_buttons button:has-text('Register Payment'):visible, "
        ".o_statusbar_buttons button:has-text('Pay'):visible, "
        "button:has-text('Register Payment'):visible"
    ).first
    pay_btn.click(force=True)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    modal_fill_field(page, "amount", "600")
    page.wait_for_timeout(400)
    modal_set_date(page, "payment_date", "06/12/2026")
    page.wait_for_timeout(400)
    if page.locator(".o-overlay-item:visible, .o_datetime_picker:visible, .o_date_picker:visible").count() > 0:
        page.press("body", "Escape")
        page.wait_for_timeout(300)
    _modal_fill_char(page, "communication", "PARTIAL-JUN-600")
    page.wait_for_timeout(400)
    modal_click_button(page, "Create Payment")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
