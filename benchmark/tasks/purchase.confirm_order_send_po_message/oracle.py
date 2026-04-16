"""Oracle for purchase.confirm_order_send_po_message."""

from benchmark.oracle_helpers import (
    click_button,
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    click_list_row(page, "MED-SEND-PO-01")
    page.wait_for_timeout(800)

    click_status_button(page, "Confirm Order")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    click_button(page, "Send PO")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last
    subject = modal.locator(".o_field_widget[name='subject'] input").first
    subject.click()
    subject.fill("")
    subject.fill("Sterling components order follow-up")
    subject.press("Tab")
    page.wait_for_timeout(400)

    body = modal.locator(
        ".o_field_widget[name='body'] .odoo-editor-editable, "
        ".o_field_widget[name='body'] [contenteditable='true']"
    ).first
    body.click()
    page.wait_for_timeout(200)
    page.keyboard.press("Control+A")
    page.wait_for_timeout(200)
    page.keyboard.press("Backspace")
    page.wait_for_timeout(200)
    page.keyboard.insert_text(
        "Please review the confirmed purchase order and reply with the delivery date today."
    )
    page.wait_for_timeout(400)

    modal.locator("button:has-text('Send')").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
