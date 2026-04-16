"""Oracle for purchase.reset_draft_edit_reconfirm."""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "Meridian Supply Co")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Update Terms and Conditions (HTML field)
    note_widget = page.locator(".o_field_widget[name='note']").first
    editor = note_widget.locator(
        "[contenteditable='true'], .note-editable, .odoo-editor-editable"
    )
    if editor.count() > 0:
        editor.first.click()
        page.wait_for_timeout(300)
        editor.first.fill("Updated via browser")
    else:
        note_widget.click()
        page.wait_for_timeout(300)
        page.keyboard.type("Updated via browser")
    page.wait_for_timeout(500)

    # Confirm the order
    confirm_btn = page.locator(
        ".o_statusbar_buttons button:has-text('Confirm Order'):visible, "
        ".o_statusbar_buttons button:has-text('Confirm'):visible"
    )
    if confirm_btn.count() > 0:
        confirm_btn.first.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)


run_oracle(oracle)
